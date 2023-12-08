test:
	pytest --cov-report term-missing --cov=source tests/

start_web_server:
	poetry run python3 source/web_server.py