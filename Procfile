web: gunicorn webScraper.wsgi --log-file -
worker: celery worker --app=core.tasks.app