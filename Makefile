export DJANGO_SETTINGS_MODULE = tests.settings
export PYTHONPATH := $(shell pwd)

test:
	pytest --cov=login_required --cov-report=term --cov-report=html

.PHONY: test
