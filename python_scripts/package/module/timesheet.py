import datetime
from typing import List

from ..utils.csv_tools import convert_row_to_object
from ..utils.schema import TimesheetCSV
from ..database.models import Timesheet
from ..database.query_wrapper import bulk_save
from ..database.repository import delete_all_timesheets


def push_timesheet_to_db(timesheets: List[TimesheetCSV]):
    """
    push timesheet to db
    """
    new_timesheets = []
    for ts in timesheets:
        data = ts.dict()
        data.pop("date")
        new_timesheets.append(Timesheet(**data))
        print(ts) if ts.total_hour < datetime.timedelta() else False

    bulk_save(new_timesheets)


def update_timesheet():
    """
    main function to update timesheets
    """
    delete_all_timesheets()
    timesheets = convert_row_to_object("../dataset/timesheets.csv", TimesheetCSV)
    push_timesheet_to_db(timesheets)
