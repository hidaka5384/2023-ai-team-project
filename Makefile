crawl:
	@poetry run scrapy crawl rakuten_recipe_spider

db_local_build:
	cd tests/docker/ && docker-compose --env-file ../../.env up -d

db_local_down:
	cd tests/docker/ && docker-compose down

data_create_table:
	@poetry run python -m tests.data.table_operations create

data_drop_table:
	@poetry run python -m tests.data.table_operations drop

install:
	@poetry install
	@poetry run pre-commit install

pre-commit-check:
	@poetry run pre-commit run --all-files

lint:
	@poetry run isort --check-only spider/
	@poetry run black spider/ --check
	@poetry run flake8 spider/
	@poetry run mypy spider/

clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

fmt:clean
	@poetry run isort spider/ tests/ yolov4/ yolov4-tiny/ utils.py
	@poetry run autoflake --in-place --recursive --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables spider/ tests/ yolov4/ yolov4-tiny/ utils.py
	@poetry run black spider/ tests/ yolov4/ yolov4-tiny/ utils.py

.PHONEY: lint clean fmt
