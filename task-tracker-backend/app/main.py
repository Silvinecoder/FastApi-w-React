import logging
import time

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.db_connection import _ENGINE, initialize_engine_and_sessionmaker
from app.assistant.model_helper import Base
from app.endpoints import users, tasks

app = FastAPI()

# Runs once at startup to build the tables
@asynccontextmanager
async def lifespan(_: FastAPI):
    max_retries = 5
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            logging.info(f"Initializing database connection (attempt {attempt+1}/{max_retries})")
            initialize_engine_and_sessionmaker(timeout=10)
            if _ENGINE is None:
                raise RuntimeError("database engine was not initialised")

            logging.info("Creating database tables")
            Base.metadata.create_all(bind=_ENGINE)
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Failed to initialize database on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("Max retries reached. Could not initialize database.")
                raise
    yield

app.include_router(users.router, prefix="/users")
app.include_router(tasks.router, prefix="/tasks")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
