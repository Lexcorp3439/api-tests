lint:
	poetry run isort .

install:
	poetry install --no-dev

install_dev:
	poetry install && \
	poetry run pre-commit install

test-async:
	pytest -n 3 -v ./tests --alluredir="./.report"

test:
	pytest -v ./tests/api --alluredir="./.report"

allure-serve:
	allure serve ./.report