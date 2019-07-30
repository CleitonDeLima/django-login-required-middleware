export DJANGO_SETTINGS_MODULE = tests.settings
export PYTHONPATH := $(shell pwd)

test:
	@coverage run `which django-admin.py` test tests
	@coverage report
	@coverage html

.PHONY: test