# PersonSite

This is a site API for any person who want to have his/her own blog and shop

## Prerequisites

To install this project you need to have the following tools installed on your PC:

* `docker`
* `docker-compose`

Also you need to create a new `.env` file in base project directory:

```
$ touch .env
```

With the following content:

```
DJANGO_SECRET_KEY="$km$wdm7+h3a=-4qftefvq+ct9@%&mc=w1^hl&!3^ekxixyjxj"
```

And if you want to interact with this project using JS, you need to add the following string in this file:

```
DJANGO_ENVIRONMENT="testing"
```

## Installing

To install this project on your PC you need to do build the Docker image first:

```
$ docker-compose build
```

After that you need to up this image

```
$ docker-compose up -d
```

And migrate the project migrations:

```
$ docker-compose run web python manage.py migrate
```

## Authors

* [Artemowkin](https://github.com/artemowkin/)

## License

This project is licensed under the [GPL-3.0](LICENSE) License
