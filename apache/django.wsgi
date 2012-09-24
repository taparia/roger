import os
import os.path
import  sys

sys.path.append('~/Desktop/Projects')
sys.path.append('~/Desktop/Projects/roger')

os.environ['PYTHON_EGG_CACHE'] ='~/Desktop/Projects/egg_cache'
os.environ['DJANGO_SETTINGS_MODULE'] = 'roger.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
