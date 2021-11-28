# TestShop

This is my testing shop project. Just for learning

## Installation

If you want to install this project you need to have the following packages:

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

## Running the project

To run the project you need to execute the following command:

```
$ python manage.py runserver
```

And the site will be available on http://127.0.0.1:8000/home/

