# myme-inventory-backend-lfpm

It is recommended to use virtual enviroment.

1. Install dependences by typing the following command.

-pip install -r requirements.txt

2. Makemigrations and migrate by typing the followig.

-python manage makemigrations
-python manage migrate

3.Create super user to get access to Admin panel.

-python manage.py createsuperuser

4. Run the server

-python manage.py runserver
