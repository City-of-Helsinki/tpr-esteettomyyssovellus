# tpr-esteettomyyssovellus

TPR Esteettömyyssovellus Backend

Requires Python 3.11+ (Docker uses Python 3.12), Django 5.2 LTS, and PostgreSQL 14+.

## to get started: Linux

## some of these steps might be optional

## install libraries to linux:

```
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0
```

## if libpq-dev doesn't work run, install dependencies manually, e.g. (NOTICE THIS IS EXAMPLE -> VERSION NUMBERS ETC):

```
sudo apt-get install libpq5=10.17-0ubuntu0.18.04.1
```

## for ~ubuntu/linux users for development it's recommended to use venv:

```
sudo apt-get install python3.12-dev
sudo apt-get install python3.12-venv
```

## to create venv (run only once/first time starting, inits the venv folder):

```
python3.12 -m venv venv
```

## activate venv (application needs to be started from venv if using it):

```
source venv/bin/activate
```

## install dependecies (without docker(?)):

```
python -m pip install --upgrade pip setuptools
python -m pip install -r requirements.txt
```

## to run the server run:

```
cd accessibility/
python manage.py runserver 0.0.0.0:8000
```

## Check the Python version in your virtualenv if dependency installation fails.

When upgrading an existing deployment, create a fresh Python 3.11+ virtualenv
instead of reusing the old Python environment. Keep deployment environment
variables and the IIS/WSGI configuration pointed at the replacement environment.
The application's WSGI entry point is unchanged.

Run the database-free upgrade regression tests from `accessibility/`:

```
python manage.py check
python manage.py test esteettomyyssovellus.api
```

## also one might need in some cases do

```
(python manage.py makemigrations)
python manage.py migrate
```


# DOCKER

Requires docker and docker-compose on the system.

To build:
./rebuild_dev.sh

To run:
./run_dev.sh

(might need sudo !!)
