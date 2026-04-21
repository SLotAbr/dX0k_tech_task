
up:
	venv/bin/python3 main.py
test:
	venv/bin/pytest -p no:warnings -vv --cache-clear ./
celery-worker:
	venv/bin/celery -A worker.celery_app worker --loglevel=info

########

migrate:
	venv/bin/alembic upgrade head
downgrade:
	venv/bin/alembic downgrade -1

