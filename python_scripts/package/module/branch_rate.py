import datetime
from typing import List, Tuple

from ..database.models import Branch_Rate
from ..database.query_wrapper import bulk_save
from ..database.repository import select_first_end_date, select_branch_salary, select_rates


def get_time_range() -> List[Tuple[datetime.datetime]]:
    """
    get time range of timesheets
    """
    first_date, end_date = select_first_end_date()

    dt1 = datetime.datetime(first_date.year, first_date.month + 1, 1)
    now: List[datetime.datetime] = [first_date, dt1 - datetime.timedelta(days=1)]
    time_range = []
    while now[0] < end_date:
        # append previous `now` to time range
        time_range.append(now)

        # use last end time as start time in the next sequence
        _, dt1 = now

        # set back to january
        year = dt1.year if dt1.month < 12 else dt1.year + 1
        month = dt1.month + 1 if dt1.month < 12 else 1
        now = [dt1, datetime.datetime(year=year, month=month, day=1)]

    return time_range


def generate_rate_key(branch_id, year, month):
    """
    generate rate key
    """
    return f"{branch_id}_{year}_{month}"


def get_rate_map():
    """
    Get rate map which mapped by unique key
    """
    branch_rates: List[Branch_Rate] = select_rates()
    rate_map = {}
    for rate in branch_rates:
        key = generate_rate_key(rate.branch_id, rate.year, rate.month)
        rate_map[key] = rate
    return rate_map

def update_branch_rate():
    """
    Update branch rate
    """
    # get rate map for update
    rate_map = get_rate_map()

    branch_rates = []
    for (start, end) in get_time_range():
        # query to db
        branch_salary = select_branch_salary(start, end)

        for bs in branch_salary:
            # calculate salary/hour
            total_hour = bs.total_work_time_sec / 3600
            salary_per_hour = bs.total_salary / bs.total_employee / total_hour

            # rate key to rate map
            rate_key = generate_rate_key(bs.branch_id, start.year, start.month)

            if rate_key in rate_map:
                rate_map[rate_key].salary_per_hour = salary_per_hour
            else:
                new_rate = Branch_Rate(
                    branch_id=bs.branch_id,
                    year=start.year,
                    month=start.month,
                    salary_per_hour=salary_per_hour
                )
                branch_rates.append(new_rate)

    # bulk save new
    bulk_save(branch_rates)
