test:
	flake8 configurations --ignore=E501,E127,E128,E124
	coverage run --branch --source=configurations manage.py test configurations
	coverage report --omit=configurations/test*
