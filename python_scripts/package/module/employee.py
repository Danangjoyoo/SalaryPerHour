from typing import Dict, List

from ..utils.csv_tools import convert_row_to_object
from ..utils.schema import EmployeeCSV
from ..utils.tools import generate_branch_name
from ..database.models import Employee, Branch
from ..database.query_wrapper import bulk_save
from ..database.repository import select_all_branch_id, select_all_employees


def group_employee_by_branch(employees: List[EmployeeCSV]):
    """
    Group hierarchy of employee
    1. branch
    2. id
    """
    branch_map = {}
    for employee in employees:
        if employee.branch_id not in branch_map:
            branch_map[employee.branch_id] = []
        branch_map[employee.branch_id].append(employee)
    return branch_map


def push_employee_and_branch_to_db(branch_map: Dict[int, List[EmployeeCSV]]):
    """
    push employee and branch to db
    """
    branch_id_list = select_all_branch_id()
    employees = select_all_employees()
    employee_map = {
        employee.employee_id: employee
        for employee in employees
    }

    new_branch_map: Dict[int, Branch] = {}
    new_employee_map: Dict[int, Employee] = {}
    for branch_id, branch_employees in branch_map.items():
        if branch_id not in branch_id_list:
            new_branch_map[branch_id] = Branch(
                branch_id=branch_id,
                branch_name=generate_branch_name()
            )

        for branch_employee in branch_employees:
            eid = branch_employee.employee_id
            if eid in employee_map:
                target_employee = employee_map[eid]
                target_employee.branch_id = branch_employee.branch_id
                target_employee.salary = branch_employee.salary
                target_employee.join_date = branch_employee.join_date
                target_employee.resign_date = branch_employee.resign_date
            else:
                new_employee_map[eid] = Employee(**branch_employee.dict())

    bulk_save(new_branch_map.values())
    bulk_save(new_employee_map.values())


def update_employee_db():
    """
    main function of updating employee
    """
    employees = convert_row_to_object("../dataset/employees.csv", EmployeeCSV)
    branch_map = group_employee_by_branch(employees)
    push_employee_and_branch_to_db(branch_map)
