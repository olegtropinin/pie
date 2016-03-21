"""
pie - Python Interactive Executor
Enables a user to execute predefined tasks that may accept parameters and options from the command line without any other required packages.
Great for bootstrapping a development environment, and then interacting with it.
"""
__VERSION__='0.0.1'

import os
import re
import subprocess
import sys
from functools import wraps


WINDOWS=(os.name=='nt')
PY3=(sys.version_info>=(3,0))


# ----------------------------------------
# configuration
# ----------------------------------------
class Lookup(object):
    """
    A class that can be used like a dictionary with more succinct syntax:
        l=Lookup(name='example',value='good')
        print(l.name)
        l.newValue=2
    """
    def __init__(self,**entries):
        self.__dict__.update(entries)


# options is a lookup object where predefined options (in code) can be placed, as well as provided on the command line.
options=Lookup()


# context is used to keep track of what context a command is being executed within.
#     with venv('venv/build'):
#         cmd('python -m pip')
context=Lookup()



# ----------------------------------------
# tasks
# ----------------------------------------
# tasks is a dictionary of registered tasks, where key=name. Tasks are possibly from within submodules where name=module.task.
tasks={}

def task(parameters=[]):
    """
    A (function that returns a) decorator that converts a simple Python function into a pie task.
     - parameters is a list of objects (use Lookup) with the following attributes:
         name - name of the param
         type - descriptive type of the param
         conversionFn - a function that will take a string and convert it to the desired type
    """
    def decorator(taskFn):
        # register the task
        tasks[taskFn.__name__]=taskFn
        # then wrap the function
        @wraps(taskFn)
        def wrapper(*args,**kwargs):
            # go through parameters and make sure they're all there, otherwise inject or prompt for them

            return taskFn(*args,**kwargs)
        return wrapper
    return decorator



# ----------------------------------------
# operations
# ----------------------------------------
def cmd(c):
    """
    Executes a system command
    """
    subprocess.call(c,shell=True)


def pip(c):
    """
    Runs a pip command
    """
    cmd('python -m pip {}'.format(c))


class venv(object):
    """
    A context class used to execute commands within a virtualenv
    """
    def __init__(self,path):
        self.path=path

    # make this a context manager
    def __enter__(self):
        # push onto pie.context
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        # pop from pie.context
        if exc_type is None:
            pass
        else:
            raise Exception('I dunno')# TODO



# ----------------------------------------
# Command line functionality
# ----------------------------------------
class Argument(object):
    def execute(self):
        print(str(self))
        # raise NotImplemented()


class Version(Argument):
    def execute(self):
        print('pie v{}'.format(__VERSION__))

    def __str__(self):
        return 'Version: {}'.format(__VERSION__)
    __repr__=__str__


class CreateBatchFile(Argument):
    def execute(self):
        if WINDOWS:
            with open('pie.bat','w') as fout:
                fout.write('@echo off\npython -c "import pie; pie.main()" %*\n')
        else:
            with open('pie','w') as fout:
                fout.write('python -c "import pie; pie.main()" %*\n')

    def __str__(self):
        return 'CreateBatchFile'
    __repr__=__str__


class Help(Argument):
    def execute(self):
        print('Usage:  pie -v | -h | -b | {-o name=value | task[(args...)]}')
        print('Version: v{}'.format(__VERSION__))
        print('')
        print('  -v    Display version')
        print('  -h    Display this help')
        print('  -b    Create batch file shortcut')
        print('  -o    Sets an option with name to value')
        print('  task  Runs a task passing through arguments if required')

    def __str__(self):
        return 'Help'
    __repr__=__str__


class Option(Argument):
    def __init__(self,name,value):
        self.name=name
        self.value=value

    def execute(self):
        setattr(options,self.name,self.value)


    def __str__(self):
        return 'Option: {}={}'.format(self.name,self.value)
    __repr__=__str__


class Task(Argument):
    def __init__(self,name,args=[],kwargs={}):
        self.name=name
        self.args=args
        self.kwargs=kwargs

    def execute(self):
        # TODO: check task arg requirements and prompt - OR - can this be done by the @task decorator?
        tasks[self.name](*self.args,**self.kwargs)

    def __str__(self):
        return 'Task: {}(args={},kwargs={})'.format(self.name,self.args,self.kwargs)
    __repr__=__str__



# ----------------------------------------
# Command line parsing
# ----------------------------------------
TASK_RE=re.compile(r'(?P<name>[^()]+)(\((?P<args>.*)\))?')
def parseArguments(args):
    # skip the name of the command
    i=1
    parsed=[]
    while i<len(args):
        arg=args[i]
        if arg=='-v':
            parsed.append(Version())
        elif arg=='-h':
            parsed.append(Help())
        elif arg=='-b':
            parsed.append(CreateBatchFile())
        elif arg=='-o':
            name,value=args[i+1].split('=')
            parsed.append(Option(name,value))
            i+=1
        else:
            mo=TASK_RE.match(arg)
            if mo:
                args=mo.group('args')
                args=args.split(',') if args else []
                # TODO: add further parsing to handle keyword arguments
                parsed.append(Task(mo.group('name'),args=args,kwargs={}))
            else:
                raise Exception('Unknown task format: {}'.format(arg))
        i+=1
    return parsed



# ----------------------------------------
# entry point
# ----------------------------------------
def main():
    args=parseArguments(sys.argv)
    if args:
        import pie_tasks
        for a in args:
            a.execute()
    else:
        Help().execute()


if __name__=='__main__':
    # import pie so that both we and any pie_tasks code that imports pie are referring to the same module variables
    import pie
    pie.main()
