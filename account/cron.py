#!/usr/bin/python
import os, sys
sys.path.append('/home/maverick/Dropbox/projects/') # the parent directory of the project
sys.path.append('/home/maverick/Dropbox/projects/medical/') # these lines only needed if not on path
os.environ['DJANGO_SETTINGS_MODULE'] = 'medical.settings'
from models import*
#from django.core.management import setup_environ
#from store import settings
#setup_environ(settings)

def test():
    a = invoice.objects.all()
    for i in a:
        print i
