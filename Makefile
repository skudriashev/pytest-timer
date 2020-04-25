black:
	black .

black-check:
	black --check .

lint:
	flake8
	black --check .

test:
	pytest -v --cov=pytest_timer --cov-report=term-missing --no-cov-on-fail tests
