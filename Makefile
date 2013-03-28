.PHONY: test release doc

test:
	flake8 configurations --ignore=E501,E127,E128,E124
	coverage run --branch --source=configurations manage.py test configurations
	coverage report --omit=configurations/test*

release:
	python setup.py sdist bdist_wheel register upload -s

doc:
	cd docs; make html; cd ..
