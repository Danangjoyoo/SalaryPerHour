from package.module.timesheet import update_timesheet
from package.module.employee import update_employee_db
from package.module.branch_rate import update_branch_rate


if __name__ == "__main__":
    update_employee_db()
    update_timesheet()
    update_branch_rate()
