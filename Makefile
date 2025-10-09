install:
	poetry install

migrations:
	python3 mediproject/manage.py makemigrations

migrate:
	python3 mediproject/manage.py migrate

runserver:
	python3 mediproject/manage.py runserver

hello:
	echo "Hello, World!"

env:
	source ./env/bin/activate

superuser:
	python3 mediproject/manage.py createsuperuser