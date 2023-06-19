CREATE TABLE `employees` (
    employee_id INTEGER NOT NULL AUTO_INCREMENT,
    branch_id INTEGER NOT NULL,
    salary INTEGER NOT NULL,
    join_date DATE NOT NULL,
    resign_date DATE,
    PRIMARY KEY (employee_id)
);


CREATE TABLE `timesheets` (
    timesheet_id INTEGER NOT NULL AUTO_INCREMENT,
    employee_id INTEGER NOT NULL,
    checkin DATETIME NOT NULL,
    checkout DATETIME NOT NULL,
    PRIMARY KEY (timesheet_id),
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);


CREATE TABLE `branches` (
    branch_id INTEGER NOT NULL AUTO_INCREMENT,
    branch_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (branch_id)
);


CREATE TABLE `branch_rate` (
    branch_rate_id INTEGER NOT NULL AUTO_INCREMENT,
    branch_id INTEGER NOT NULL,
    `year` YEAR NOT NULL,
    `month` INTEGER NOT NULL,
    salary_per_hour FLOAT NOT NULL,
    PRIMARY KEY (branch_rate_id),
    FOREIGN KEY (branch_id) REFERENCES branches (branch_id)
);
