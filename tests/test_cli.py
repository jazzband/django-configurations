import os
import subprocess

PROJECT_DIR = os.getcwd()
TEST_PROJECT_DIR = os.path.join(PROJECT_DIR, 'test_project')


def test_configuration_argument_in_cli():
    """Verify that's configuration option has been added to managements commands"""
    os.chdir(TEST_PROJECT_DIR)
    p = subprocess.Popen(['python', 'manage.py', 'test',
                          '--help'], stdout=subprocess.PIPE)
    assert '--configuration' in p.communicate()[0].decode('UTF-8')
    p = subprocess.Popen(['python', 'manage.py', 'runserver',
                          '--help'], stdout=subprocess.PIPE)
    assert '--configuration' in p.communicate()[0].decode('UTF-8')
    os.chdir(PROJECT_DIR)
