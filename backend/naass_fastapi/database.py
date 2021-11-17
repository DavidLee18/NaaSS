from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#mysql+pymysql://{username}:{password}@{host}:{port}/{db}
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://naass_user:NaaSS!%40#$0987@141.164.45.196:3306/naass_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=300)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
