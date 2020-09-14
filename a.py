import inspect
def b():
    print(inspect.stack()[1].function)
def a():
    b()
a()