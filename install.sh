pip install -r requirements.txt
bower install

cd tickets_project

./manage.py syncdb
./manage.py collectstatic
