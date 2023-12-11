SHELL = /bin/bash

test:
	poetry run pytest --cov-report term-missing --cov=source tests/

start:
	poetry run python3 source/web_server.py

lint:
	poetry run pylint source/

