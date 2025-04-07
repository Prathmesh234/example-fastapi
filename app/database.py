from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session
from .config import settings
##this is also the older version of sqlalchemy. Remember a lot of things have changed since then
# connection string = "postgresql://database_name:password/hostname/db_name" 
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db= SessionLocal()
    try: 
        yield db
    finally:
        db.close()



'''

If we want to use the raw sql queries rather than the ORM, we can use the psycopg2 library to connect to the database.
##cursor factory makes everything just look pretty/dictionary type format 
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Prathmesh2002#', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        ##cursor will be used to execute sql statements 
        print("Connected to the database")
        break
    except Exception as e:
        print("Connection to database failed")
        print("Error: ", e)
        time.sleep(2)
        

'''