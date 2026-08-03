.PHONY: test
test:
	uv run pytest --cov=crawler --cov-report=xml --cov-report=term-missing -vvv

.PHONY: format
format:
	uv run black -l 89 tests app

.PHONY: check
check:
	uv run black -l 89 --check tests app
