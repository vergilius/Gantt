Gantt
=====

Project management system with gantt charts

Setup ( skip if you don't need VM )
- cd vagrant && vagrant up
- vagrant ssh
- cd /var/www/gantt_project/gantt
- ./manage.py syncdb
- ./manage.py migrate
- ./manage.py runserver 127.0.0.1:3000

