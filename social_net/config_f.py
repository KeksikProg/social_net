from multiprocessing import cpu_count

command = 'home/maxek/django/env/bin/gunicorn'
pythonpath = 'home/maxek/django/social_net/social_net'
bind = '0.0.0.0:1448'
workers = cpu_count() * 2 + 1
user = 'maxek'
limit_request_fields = 3000
raw_env = 'DJANGO_SETTINGS_MODULE=social_net.settings'
