# myapp setup

## Use these commands on your terminal
python -m venv .my_env
 source my_env/bin/activate
 cd myapp/
 python3 manage.py makemigrations
 python3 manage.py migrate
 python3 manage.py createsuperuser
 python3 manage.py runserver