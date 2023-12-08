test:
	export PYTHONPATH=$PWD
	poetry run pytest --cov-report term-missing --cov=source tests/

start:
	export PYTHONPATH=$PWD
	poetry run python3 source/web_server.py

lint:
	export PYTHONPATH=$PWD
	poetry run pylint source/