# The Glinteco Showoff Project

Project for showing off capability of Glinteco Company

## Prepare environment

### Create a virtual environment

```bash
pyenv virtualenv student_management
pyenv shell student_management

# or

python -m venv venv
source venv/bin/activate
```

### Install poetry

- poetry is used for easily managing dependency packages

```bash
pip install poetry
```

### Install dependency packages

```bash
poetry install

# for development
poetry install --dev
```

### Create Database

If using sqlite, you can pass this step.
This guide intends to help create PostgreSQL db

```sql
DROP DATABASE IF EXISTS student_management;

CREATE DATABASE student_management;

CREATE ROLE student_management WITH LOGIN PASSWORD 'password';
ALTER DATABASE student_management OWNER TO student_management;
```

### Create environment file

``` bash
cp .env.tpl .env

# Update the environment varables as needed
```

### Run migrate to init database for the app

```bash
python manage.py migrate
```

## Create superuser

```bash
python manage.py createsuperuser
```

### Install pre-commit

```bash
# cd <TO REPO's root directory>
pre-commit install
```

### Run mypy for checking type annotations

```bash
mypy --ignore-missing-imports
```

### Install redis if needed

```bash
# For Ubuntu
## Install redis
sudo apt-get install redis-server
## Start service
sudo service redis-server

# For Mac
## Install redis
brew install redis
## Start service
brew services start redis
```


## Run celery

```bash
ENVIRONMENT=local celery -A student_management.celery_tasks worker -l info -Q default
ENVIRONMENT=local celery -A student_management.celery_tasks beat -l info
```

## Run flower to easily manage celery in browsers

```bash
# Run flower to manage celery
ENVIRONMENT=local celery -A student_management.celery_tasks flower
```

Then navigate to http://localhost:5555/
