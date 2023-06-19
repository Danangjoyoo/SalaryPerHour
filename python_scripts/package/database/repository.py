import datetime
from typing import List
from sqlalchemy import select, func, asc, desc, delete
from .models import Employee, Branch, Branch_Rate, Timesheet
from .query_wrapper import get_all, get_scalar_all, get_first, execute

def select_all_branch_id():
    """
    SELECT b.branch_id FROM Branches;
    """
    branch_id_list = get_scalar_all(select(Branch.branch_id))
    return branch_id_list

def select_all_employees():
    """
    SELECT * FROM Employees;
    """
    employees = get_scalar_all(select(Employee))
    return employees

def select_first_end_date():
    """
    SELECT
        ts.checkin
    FROM Timesheets ts
    ORDER BY ts.checkin ASC
    LIMIT 1;

    SELECT
        ts.checkout
    FROM Timesheets ts
    ORDER BY ts.checkin DESC
    LIMIT 1;
    """
    query1 = select(
        Timesheet.checkin
    ).order_by(
        asc(Timesheet.checkin)
    )
    timesheet = get_first(query1)
    min_date = timesheet.checkin

    query2 = select(
        Timesheet.checkout
    ).order_by(
        desc(Timesheet.checkout)
    )
    timesheet = get_first(query2)
    max_date = timesheet.checkout

    return min_date, max_date


def select_branch_salary(time_start: datetime.datetime, time_end: datetime.datetime):
    """
    SELECT
        b.branch_id,
        count(ee.employee_id) as `total_employee`,
        sum(ee.total_sec)
    FROM branches b
    JOIN (
        SELECT
            e.employee_id,
            e.branch_id,
            sum(time_to_sec(timediff(ts.checkout, ts.checkin))) as `total_sec`
        FROM employees e
        JOIN timesheets ts on ts.employee_id = e.employee_id
        WHERE
            "2019-08-21 00:00:00" < ts.checkin
            and "2020-08-21 00:00:00" > ts.checkout
        GROUP BY e.employee_id
    ) as ee on ee.branch_id = b.branch_id
    GROUP BY b.branch_id;
    """
    employee_subquery = select(
        Employee.employee_id,
        Employee.branch_id,
        Employee.salary,
        func.sum(func.time_to_sec(
            func.timediff(Timesheet.checkout, Timesheet.checkin)
        )).label("work_time_sec")
    ).join(
        Timesheet,
        Timesheet.employee_id == Employee.employee_id
    ).filter(
        time_start <= Timesheet.checkin,
        Timesheet.checkout < time_end
    ).group_by(
        Employee.employee_id
    ).subquery()

    query = select(
        Branch.branch_id,
        func.count(employee_subquery.c.employee_id).label("total_employee"),
        func.sum(employee_subquery.c.salary).label("total_salary"),
        func.sum(employee_subquery.c.work_time_sec).label("total_work_time_sec"),
    ).join(
        employee_subquery,
        employee_subquery.c.branch_id == Branch.branch_id
    ).group_by(
        Branch.branch_id
    )

    result = get_all(query)
    return result


def select_rates() -> List[Branch_Rate]:
    """
    SELECT * from Branch_Rate;
    """
    result = get_all(select(Branch_Rate))
    result = [r[0] for r in result] if result else []
    return result

def delete_all_timesheets():
    """
    DELETE FROM Timesheets;
    """
    execute(delete(Timesheet))
