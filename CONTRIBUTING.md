# Contribution guide

If you want to contribute this project, you need to read this document

## Type of contributions

If you're a frontend developer, you need to read the
[Frontend developers guide](#frontend-developers-guide) section.
If you're a backend developer, you need to read the 
[Backend developers guide](#backend-developers-guide) section

## Frontend developers guide

### Prerequisites

Create the `.env` file in base project directory with the following content:

```
DJANGO_SECRET_KEY="$km$wdm7+h3a=-4qftefvq+ct9@%&mc=w1^hl&!3^ekxixyjxj"
DJANGO_ENVIRONMENT="testing"
```

### Installing

Ok, you just want to use this project as RESTful backend. For this you need
to install `docker` and `docker-compose` (if not installed) and run the following
commands in base project directory:

```
$ docker-compose build
$ docker-compose up -d
```

For first time after building, and after pulling updates, you need to run the
following command:

```
$ docker-compose run web python manage.py migrate
```

And, if you want to have permission to send POST, PUT, DELETE and etc. requests,
you need to create a superuser:

```
$ docker-compose run web python manage.py createsuperuser
```

After running of this command you cat interact with console. Enter the following:

```
Username (leave blank to use 'root'): admin
Email address: admin@gmail.com
Password: admin
Password (again): admin
...
Bypass password validation and create user anyway? [y/N]: y
```

And now you have user with email (`admin@gmail.com`) and password (`admin`) that
you can use to log in and interact with API

> You need to run the `createsuperuser` command **ONLY ONCE**

### Running

To run the installed project you need to run the following command:

```
$ docker-compose up -d
```

And go to the http://localhost:8000/

If you want to stop the project, you can do the following:

```
$ docker-compose down
```

### Documantation

API documentation is located on `/docs/` endpoint

## Backend developers guide