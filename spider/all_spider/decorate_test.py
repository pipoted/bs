def wraping(func):
    def inner(args, kwargs):
        print('test start')
        func(args, kwargs)
        print(func.__name__)
        print('test end')

    return inner

@wraping
def test(a, b):
    print(a, b)


test(1, 2)
