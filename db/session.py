from sqlalchemy import create_engine

DB = "events_db"
PORT = "5432"
HOST = "db"
PASSWORD = "password"
USER = "postgres"
DB_TYPE = "postgresql"


SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
