source /home/maxek/django/env/bin/activate
gunicorn -c '/home/maxek/django/social_net/config_f.py' social_net.wsgi
