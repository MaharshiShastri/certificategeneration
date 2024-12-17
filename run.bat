if (pip list| grep waitress) then
    pip install waitress

python manage.py makemigrations
python manage.py migrate
waitress-serve --port=8000 shantabai_login.wsgi:application
