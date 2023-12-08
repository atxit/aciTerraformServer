test:
	export PYTHONPATH=$PWD
	poetry run pytest --cov-report term-missing --cov=source tests/

start_web_server:
	export PYTHONPATH=$PWD
	poetry run python3 source/web_server.py