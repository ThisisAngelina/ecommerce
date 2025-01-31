web: python manage.py migrate && gunicorn ecommerce.wsgi --log-file -
worker: celery -A ecommerce worker --loglevel=info