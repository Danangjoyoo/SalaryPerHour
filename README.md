# Salary per hour

## Assumptions
- 2 shift
    - morning shift: 9-17
    - night shift: 17-9
- if duplicated employee, wil take the latest one

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