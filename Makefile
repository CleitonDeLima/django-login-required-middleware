coverage:
	python -m pytest --cov-report=html


publish:
	# install twine
	python setup.py sdist
	twine upload dist/*
