from pie import *

import inModule


@task()
def asdf(v):
    """Test task."""
    print('whoo'+v)


@task()
def noDesc():
    pass


@task()
def a_long_long_long_long_long_long_task_name():
    """And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    """
    print('long')


@task
def testCmd():
    cmd('echo hi')


def not_a_task():
    pass


@task
def useVenv():
    with venv('venv'):
        # cmd('python')
        pip('install humanize==0.5.1')
