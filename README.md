# TestShop

This is my testing shop project. Just for learning

## Installation

### Using docker

If you want just to install this project on your local machine you can
run it as a docker container. So, you need the following packages:

* `docker`
* `docker-compose`

Ok. Build the docker image:

```
$ docker-compose build
```

Up this image:

```
$ docker-compose up -d
```

And apply all migrations (do this only one time):

```
$ docker-compose run web python manage.py migrate
```

And, if you want, you can create a superuser to get acces to admin panel:

```
$ docker-compose run web python manage.py createsuperuser
```

And go on http://127.0.0.1:8000/

### Using Python and poetry

If you want to install this project to contribute the developing
you need to have the following packages:

* [Python >= 3.9](https://www.python.org/downloads/release/python-390/)
* [Poetry](https://python-poetry.org/docs/#installation)

If you already have these packages you need to install poetry dependencies:

```
$ poetry install
```

After that create a new `.env` file in home project directory with
the following content:

```
DJANGO_SECRET_KEY="2$6#ajqdl8n+-6qs6f#))pivv&hku5rj37iy$y@swp6$v)7+9v"
```

And run the following commands:

```
$ poetry shell
$ export $(cat .env | xargs)
```

Apply all migrations:

```
$ python manage.py migrate
```

And create the superuser:

```
$ python manage.py createsuperuser
```

To run the project you need to execute the following command:

```
$ python manage.py runserver
```

And the site will be available on http://127.0.0.1:8000/

## Running the tests

### Unit tests

To run unit tests you can do the following:

```
$ python manage.py test cart orders products reviews
```

### Functional tests

If you want to run functional tests for the project you need to have
`geckodriver` on your machine first. And, if it's ok, you can run the
following command:

```
$ python manage.py test functional_tests
```

## Authors

* **Artemowkin** - https://github.com/artemowkin/

## License

This project is licensed under the GPL-3.0 License -
see the [LICENSE](LICENSE) file for details

