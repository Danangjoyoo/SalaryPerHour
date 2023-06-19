
CREATE TEMPORARY TABLE temp_table_employee (
    employee_id INTEGER,
    branch_id INTEGER,
    salary INTEGER,
    join_date DATE,
    resign_date DATE
);

LOAD DATA INFILE '/dataset/employees.csv'
INTO TABLE temp_table_employee
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@var1, @var2, @var3, @var4, @var5)
SET
    employee_id = @var1,
    branch_id = @var2,
    salary = @var3,
    join_date = @var4,
    resign_date = case
        when @var5 != "" then @var5
        else null
    end
;

INSERT INTO employees
SELECT tte.employee_id, tte.branch_id, tte.salary, tte.join_date, tte.resign_date
FROM temp_table_employee tte
ON DUPLICATE KEY UPDATE salary = tte.salary;



LOAD DATA INFILE '/dataset/timesheets.csv'
INTO TABLE timesheets
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@var1, @var2, @var3, @var4, @var5)
SET
    timesheet_id = @var1,
    employee_id = @var2,
    checkin = CONCAT(@var3, " ", @var4),
    checkout = CONCAT(@var3, " ", @var5)
;
