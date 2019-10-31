[![Build Status](https://travis-ci.com/kraglalbert/budgie-web.svg?branch=master)](https://travis-ci.com/kraglalbert/budgie-web)
# Budgie

A web-based application to allow individuals to easily track their monthly expenses.

## Setup

Set up a Python virtual environment for the backend:
```
python3 -m venv env

source env/bin/activate 
```

Once the environment is activated, install dependencies:

```
pip install -r /path/to/requirements.txt
```

## Backend

To run the backend from the `backend` folder:

```
python manage.py runserver
```

To run tests:

```
python manage.py test
```

A `.env` file is required to define all necessary environment variables. The file should at minimum set `FLASK_CONFIG`, `DEV_DATABASE_URL`, `TEST_DATABASE_URL` and `SECRET_KEY`.

