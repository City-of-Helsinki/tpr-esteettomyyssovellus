# tpr-esteettomyyssovellus

TPR Esteettömyyssovellus Backend

requires python 3.9 and django 3.2.3

## to get started: Linux

## some of these steps might be optional

## install libraries to linux:

```
sudo apt-get install postgresql
sudo apt-get install libpq-dev
sudo apt-get install python-psycopg2
```

## if libpq-dev doesn't work run, install dependencies manually, e.g. (NOTICE THIS IS EXAMPLE -> VERSION NUMBERS ETC):

```
sudo apt-get install libpq5=10.17-0ubuntu0.18.04.1
```

## for ~ubuntu/linux users for development it's recommended to use venv:

```
sudo apt-get install python3.9-dev
sudo apt-get install python3.9-venv
```

## to create venv (run only once/first time starting, inits the venv folder):

```
python3.9 -m venv venv
```

## activate venv (application needs to be started from venv if using it):

```
source venv/bin/activate
```

## install dependecies (without docker(?)):

```
pip install -r requirements.txt
```

## to run the server run:

```
cd accessibility/
python manage.py runserver 0.0.0.0:8000
```

## if nothing seems to work double check: venv python version :D hours used: 3 (+ dependencies)

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
