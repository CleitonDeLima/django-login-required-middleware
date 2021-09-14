export DJANGO_SETTINGS_MODULE = tests.settings
export PYTHONPATH := $(shell pwd)

test:
	pytest --cov=login_required --cov-report=term --cov-report=xml --cov-report=term-missing

publish:
	# install twine
	python setup.py sdist
	twine upload dist/*

.PHONY: test
