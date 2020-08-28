web: gunicorn webScraper.wsgi --log-file -
worker: celery -A core.tasks worker -B --loglevel=info
python manage.py celeryd -v 2 -B -s celery -E -l INFO