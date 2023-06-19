from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://local:local123@localhost:3306/companydb")
session = sessionmaker(engine, autocommit=False)
