web: gunicorn webScraper.wsgi --log-file -
worker: celery worker --app=tasks.app