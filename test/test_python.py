from functools import wraps

# def decorator_outer(func):
#     print('decorator outer')
#     def wrapper(*args):
#         print('111', func)
#         return func(*args)
#     return wrapper
#
def decorator_inner(func):
    print('decorator inner')
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('111', func)
        print(args, kwargs)
        return func(*args, **kwargs)
    return wrapper

# @decorator_outer
@decorator_inner
def fun_1(*args, **kwargs):
    print('fun_1', args, kwargs)
    print(fun_1)
    return 1

if __name__ == '__main__':
    fun_1(1, 2, key1='ate', key2='te')








