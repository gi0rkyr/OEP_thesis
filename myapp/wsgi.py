"""
WSGI config for myapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import socketio
import eventlet
import eventlet.wsgi
from main.views import sioh
#from containers.views import sio

django_app = get_wsgi_application()
#application_containers = socketio.WSGIApp(sio, django_app)
application_main = socketio.WSGIApp(sioh, django_app)

#eventlet.wsgi.server(eventlet.listen(('', 8000)), application_containers)
eventlet.wsgi.server(eventlet.listen(('', 8000)), application_main)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

# https://github.com/miguelgrinberg/python-socketio/blob/main/examples/server/wsgi/django_socketio/django_socketio/wsgi.py
# https://studygyaan.com/django/how-to-use-python-socket-io-with-django
