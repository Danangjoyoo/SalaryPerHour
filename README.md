# Salary per hour

## Assumptions
- there are 2 shifts
    - morning shift: 09:00 - 17:00
    - night shift: 17:00 - 09:00
- if duplicated employee, wiLl take the latest one
- any new csv files will always named `employees.csv` and `timesheets.csv`, and will be placed under `/dataset` directory

## How to deploy?
1. make sure you have docker installed in your machine
2. make sure you have docker compose installed
3. serve up docker container
```
docker-compose up --build
```

## How to run python script? (Linux)
1. setup virtualenv
```
python3 -m virtualenv venv
```
2. activate venv and install reqs
```
. ./venv/bin/activate
```
3. install
```
pip install -r python_scripts/requirements.txt
```
4. run in the working directory
```
cd ./python_scripts && python main.py
```


## How to run SQL script?
```bash
docker exec -it de_database bash -c "mysql -u root -proot123 companydb < /scripts/command.sql"
```