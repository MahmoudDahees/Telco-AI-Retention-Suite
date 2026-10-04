import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

url = os.getenv("DB_URL", "sqlite:///./customers.db")
connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
engine = create_engine(url=url, connect_args=connect_args)
Sessionlocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()
