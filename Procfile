web: gunicorn config.wsgi:application
worker: celery worker --app=sparta_webapp.taskapp --loglevel=info
