#!/usr/bin/env bash

apt-get update
apt-get install -y python
apt-get install -y python-pip

cd /var/www/gantt_project
pip install -r requirements.txt

# well, this shit ain't gonna work this way...
#cd gantt
#./manage.py syncdb
#./manage.py migrate
#./manage.py runserver 127.0.0.1:80
