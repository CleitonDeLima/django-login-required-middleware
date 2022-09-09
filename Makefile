coverage:
	python -m pytest --cov=login_required --cov-report=html --cov-report=term-missing


publish:
	# install twine
	python setup.py sdist
	twine upload dist/*
