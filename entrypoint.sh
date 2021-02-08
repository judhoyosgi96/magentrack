#!/bin/bash
python /code/manage.py makemigrations
python /code/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python /code/manage.py shell

echo "from apps.variable.models import Variable; Variable.objects.update_or_create(id=0,name='items_per_page',value='5')" | python /code/manage.py shell

python /code/manage.py runserver 0.0.0.0:8000
