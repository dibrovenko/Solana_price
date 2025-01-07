from dotenv import load_dotenv
import os

load_dotenv()

database_config = {
    "host": os.getenv("HOST"),
    "port": 5432,
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "db_name": os.getenv("POSTGRES_DB"),
    "type_connect": "asyncpg",
    "type_db": "postgresql"
}
