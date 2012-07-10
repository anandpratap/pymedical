import os
import sys
path = '/home/maverick/Dropbox/projects'
sys.path.append('/home/maverick/envs/maverick/lib/python2.7')
sys.path.append('/home/maverick/envs/maverick/lib/python2.7/site-packages')
sys.path.append('/home/maverick/envs/maverick/lib/python2.7/site-packages/Django-1.3-py2.7.egg/')

if path not in sys.path:
    sys.path.append(path)
sys.path.append('/home/maverick/Dropbox/projects/medical')
os.environ['DJANGO_SETTINGS_MODULE'] = 'medical.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()