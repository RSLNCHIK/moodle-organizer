from sqlalchemy import text
from .database import engine

with engine.connect() as connection:
    # Execute a simple query to check the connection
    result = connection.execute(text("SELECT 1"))

    print("Database connection successful. Result: ", result.scalar())