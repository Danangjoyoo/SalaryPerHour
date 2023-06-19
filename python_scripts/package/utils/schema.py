import datetime
from pydantic import BaseModel, validator
from typing import Optional, Union


class EmployeeCSV(BaseModel):
    employee_id: int
    branch_id: int
    salary: int
    join_date: datetime.date
    resign_date: Union[float, datetime.date]

    @validator("resign_date")
    def validate_resign_date(cls, value):
        if str(value) == "nan":
            return None
        return value


class TimesheetCSV(BaseModel):
    timesheet_id: int
    employee_id: int
    date: datetime.date
    checkin: Union[Optional[datetime.datetime], str]
    checkout: Union[Optional[datetime.datetime], str]

    @property
    def total_hour(self):
        return self.checkout - self.checkin

    @validator("date")
    def validate_date(cls, value):
        if str(value) == "nan":
            return None
        return value

    @validator("checkin")
    def validate_checkin(cls, value, values):
        if str(value) == "nan":
            value = "09:00:00"
        return cls.get_check_datetime(values["date"], value)

    @validator("checkout")
    def validate_checkout(cls, value, values):
        if str(value) == "nan":
            value = "17:00:00"

        out = cls.get_check_datetime(values["date"], value)
        if values["checkin"] <= out:
            return out
        else:
            return cls.get_check_datetime(
                values["date"] + datetime.timedelta(days=1),
                "09:00:00"
            )


    @classmethod
    def get_check_datetime(cls, date_, time_str):
        time_ = datetime.datetime.strptime(time_str, "%H:%M:%S")
        datetime_ = datetime.datetime(
            date_.year, date_.month, date_.day,
            time_.hour, time_.minute, time_.second
        )
        return datetime_
