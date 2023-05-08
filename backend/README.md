### Helper Commands

1. To run the server from the api directory,

```
uvicorn app.main:app --reload
```

2. Build a new image and spin up containers

```
docker-compose up -d --build
```

3. Access the database via psql

```
docker-compose exec web-db psql -U postgres
```

4. Pull containers and volumes down

```
docker-compose down -v
```

5. Docker destroy and build

```
docker-compose down -v && docker-compose up -d --build
```

6. Initialize Migration

```
docker-compose exec web aerich init -t app.db.TORTOISE_ORM
```

7. Initialize db

```
docker-compose exec web aerich init-db
```

8. Run pytest

```
docker-compose exec web python -m pytest
```

9. Generate schema for database

```
docker-compose exec web python app/db.py
```

10. Apply Migrations

```
docker-compose exec web aerich upgrade
```

11. Check available endpoints

```
Navigate to http://localhost:8000/docs#/
```
