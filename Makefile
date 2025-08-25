.PHONY: run migrate createsuperuser loaddata test lint

run:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py makemigrations
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser

loaddata:
	python manage.py loaddata fixtures/initial_data.json

test:
	pytest -v --disable-warnings

lint:
	flake8 .
