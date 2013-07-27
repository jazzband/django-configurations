from invoke import run, task


@task
def test(label='configurations'):
    run('flake8 configurations --ignore=E501,E127,E128,E124')
    run('./manage.py test {0} -v2'.format(label))


@task
def release():
    run('python setup.py sdist bdist_wheel register upload -s')


@task
def docs():
    run('cd docs; make html; cd ..')
