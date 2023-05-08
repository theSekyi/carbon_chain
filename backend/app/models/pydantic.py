from datetime import date

from pydantic import BaseModel, Field


class EfficiencyByType(BaseModel):
    ship_type: str
    average_technical_efficiency: float


class DateRangeSummary(BaseModel):
    start_date: date
    end_date: date
    total_co2_emissions: float
    average_co2_emissions_per_distance: float
    average_technical_efficiency: float
