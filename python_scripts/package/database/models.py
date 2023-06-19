from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import YEAR

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=False)
    salary = Column(Integer, nullable=False)
    join_date = Column(Date, nullable=False)
    resign_date = Column(Date, nullable=True)

class Timesheet(Base):
    __tablename__ = "timesheets"
    timesheet_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    checkin = Column(DateTime, nullable=False)
    checkout = Column(DateTime, nullable=False)

class Branch(Base):
    __tablename__ = "branches"
    branch_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_name = Column(String(100), nullable=False, unique=True)

class Branch_Rate(Base):
    __tablename__ = "branch_rate"
    branch_rate_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"))
    year = Column(YEAR, nullable=False)
    month = Column(Integer, nullable=False)
    salary_per_hour = Column(Float, nullable=False)
