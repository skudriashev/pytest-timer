black:
	black .

black-check:
	black --check .

deps:
	pip install -r dev-requirements.txt

lint:
	flake8
	black --check .

test:
	pytest -v --cov=pytest_timer --cov-report=term-missing --no-cov-on-fail tests
