from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import time
 
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
print(SQLALCHEMY_DATABASE_URL)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",database= 'fastapi', user='posts', password= 'PostgreS', cursor_factory=RealDictCursor )
#         cursor = conn.cursor()
#         print('Database Connection was successful')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print("error:", error)
#         time.sleep(2)
