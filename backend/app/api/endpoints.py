import re
import sys
from datetime import date
from typing import Dict, List, Tuple

from app.models.models import Ship, Ship_Pydantic, ShipIn_Pydantic
from app.models.pydantic import DateRangeSummary, EfficiencyByType
from fastapi import APIRouter, HTTPException, Query
from tortoise.expressions import F
from tortoise.functions import Avg, Count, Sum

router = APIRouter()


import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger.addHandler(handler)


@router.get("/", response_model=Tuple[int, List[Ship_Pydantic]])
async def get_ships(skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000)):
    """
    Retrieve a paginated list of ships and the total count of ships.

    This function returns a tuple containing the total number of ships in the database
    and a list of `Ship_Pydantic` objects representing the paginated ships for the
    specified page. The `skip` and `limit` query parameters are used for pagination.

    Args:
        skip (int, optional): Number of items to skip before starting to return the results.
                              Defaults to 0.
                              Must be greater than or equal to 0.
        limit (int, optional): Maximum number of items to return in the response.
                               Defaults to 1000.
                               Must be between 1 and 1000.

    Returns:
        Tuple[int, List[Ship_Pydantic]]: A tuple containing the total count of ships and the
                                         paginated list of ships as `Ship_Pydantic` objects.

    Raises:
        HTTPException: If no ships are found, raises a 404 error with a "No ships found" detail.
    """
    total_count = await Ship.all().count()
    ships = await Ship_Pydantic.from_queryset(Ship.all().offset(skip).limit(limit))

    if not ships:
        raise HTTPException(status_code=404, detail="No ships found")

    return total_count, ships


@router.get("/{id}", response_model=Ship_Pydantic)
async def get_ship_by_id(id: int):
    """
    Retrieve a ship's details by its ID.

    Args:
        id (int): The unique identifier of the ship to be retrieved.

    Returns:
        Ship_Pydantic: A Pydantic model representing the ship's details.
        If the ship with the given ID is not found, a 404 error with a
        "Ship not found" message is returned.

    Raises:
        HTTPException: Raised when the ship with the given ID is not found
        in the database. The exception includes a 404 status code and a
        "Ship not found" detail message.
    """
    retrieved_ship = await Ship.get_or_none(id=id)
    if not retrieved_ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return await Ship_Pydantic.from_tortoise_orm(retrieved_ship)


@router.post("/", response_model=Ship_Pydantic)
async def create_ship(ship: ShipIn_Pydantic):
    """
    Add a new ship with its details.

    Args:
        ship (ShipIn_Pydantic): The ship details to be added, as a Pydantic model.

    Returns:
        Ship_Pydantic: A Pydantic model representing the newly created ship's details.
    """
    # Check for duplicate ship names
    existing_ship = await Ship.get_or_none(name=ship.name)
    if existing_ship:
        raise HTTPException(status_code=400, detail="Ship with this name already exists")

    # Create the ship and handle database errors
    try:
        ship_obj = await Ship.create(**ship.dict(exclude_unset=True))
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Failed to create ship: {str(e)}")

    return await Ship_Pydantic.from_tortoise_orm(ship_obj)


@router.put("/{id}", response_model=Ship_Pydantic)
async def update_ship_by_id(id: int, updated_ship: ShipIn_Pydantic):
    """
    Update a specific ship's details by its ID.

    Args:
        id (int): The unique identifier of the ship to be updated.
        updated_ship (ShipIn_Pydantic): The ship details to be updated, as a Pydantic model.

    Returns:
        Ship_Pydantic: A Pydantic model representing the updated ship's details.
        If the ship with the given ID is not found, a 404 error with a
        "Ship not found" message is returned.

    Raises:
        HTTPException: Raised when the ship with the given ID is not found
        in the database. The exception includes a 404 status code and a
        "Ship not found" detail message.
    """
    ship = await Ship.get_or_none(id=id)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")

    await ship.update_from_dict(updated_ship.dict(exclude_unset=True)).save()
    return await Ship_Pydantic.from_tortoise_orm(ship)


@router.delete("/{id}", response_model=Ship_Pydantic)
async def delete_ship_by_id(id: int):
    """
    Delete a specific ship by its ID.

    Args:
        id (int): The unique identifier of the ship to be deleted.

    Returns:
        Ship_Pydantic: A Pydantic model representing the deleted ship's details.
        If the ship with the given ID is not found, a 404 error with a
        "Ship not found" message is returned.

    Raises:
        HTTPException: Raised when the ship with the given ID is not found
        in the database. The exception includes a 404 status code and a
        "Ship not found" detail message.
    """
    ship = await Ship.get_or_none(id=id)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")

    deleted_ship = await Ship_Pydantic.from_tortoise_orm(ship)
    await ship.delete()
    return deleted_ship


@router.get("/type/{ship_type}", response_model=list[Ship_Pydantic])
async def get_ships_by_type(
    ship_type: str,
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    page_size: int = Query(1000, ge=1, le=1000, description="Number of items per page (1-1000)"),
):
    """
    Retrieve a list of ships filtered by ship type, with pagination.

    Args:
        ship_type (str): The ship type to filter the ships by.
        page (int): The page number to retrieve (default: 1).
        page_size (int): The number of items to return per page (default: 1000).

    Returns:
        List[Ship_Pydantic]: A list of Pydantic models representing the ships with the specified ship type.

    Raises:
        HTTPException: Raised when no ships with the specified ship type are found
        in the database. The exception includes a 404 status code and a
        "No ships found with the specified ship type" detail message.
    """
    ship_type_exists = await Ship.filter(ship_type=ship_type).exists()
    if not ship_type_exists:
        raise HTTPException(status_code=404, detail="No ships found with the specified ship type")

    offset = (page - 1) * page_size

    ships = await Ship_Pydantic.from_queryset(Ship.filter(ship_type=ship_type).offset(offset).limit(page_size))

    return ships


@router.get("/reporting-period/{reporting_period}", response_model=list[Ship_Pydantic])
async def get_ships_by_reporting_period(
    reporting_period: str,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(1000, ge=1, le=1000, description="Number of items to return (1-1000)"),
):
    """
    Retrieve a list of ships filtered by the reporting period, with pagination.

    Args:
        reporting_period (str): The reporting period to filter the ships by in the format YYYY-MM-DD.
        skip (int): The number of items to skip (default: 0).
        limit (int): The number of items to return (default: 1000).

    Returns:
        List[Ship_Pydantic]: A list of Pydantic models representing the ships with the specified reporting period.

    Raises:
        HTTPException: Raised when no ships with the specified reporting period are found
        in the database or when the reporting period format is invalid.
        The exception includes a 404 or 400 status code and a detail message.
    """
    # Validate reporting period format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", reporting_period):
        raise HTTPException(status_code=400, detail="Invalid reporting period format")

    retrieved_ships = await Ship_Pydantic.from_queryset(
        Ship.filter(reporting_period=reporting_period).offset(skip).limit(limit)
    )

    if not retrieved_ships and skip == 0:
        raise HTTPException(status_code=404, detail="No ships found with the specified reporting period")

    return retrieved_ships

