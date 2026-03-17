# Decorator
# import numbers

# def decorator_function(original_function):
#     def wrapper_function(*args, **kwargs):
#         print("Before")
#         print(args)
#         print(kwargs)
#         result = original_function(*args, **kwargs)
#         print(f"Function result: {result}")
#         print("After")
#         return result
#     return wrapper_function
#
#
# @decorator_function
# def my_function(number1, number2):
#     return number1 + number2
#
# @decorator_function
# def other_function(number1, number2, number3):
#     return number1 * number2 - number3


# print(my_function(1, 2))
# print(other_function(165, 2, 98))


# authenticate example
# def is_authenticate():
#     return False
#
#
# def check_authenticate(func):
#     def wrapper(*args, **kwargs):
#         if is_authenticate():
#             print("User authenticated")
#             return func(*args, **kwargs)
#         else:
#             raise Exception("User unauthenticated")
#     return wrapper
#
#
# @check_authenticate
# def do_something():
#     print("Do something")
#
# do_something()

# validate example
# def validate_arguments(func):
#     def wrapper(*args, **kwargs):
#         for arg in [*args, *kwargs.values()]:
#             if not isinstance(arg, int):
#                 raise TypeError(f"Argument must be an integer: {arg}")
#         return func(*args, **kwargs)
#     return wrapper
#
#
# @validate_arguments
# def summ(a, b):
#     return a + b
#
#
# print(summ(1, 2))
# print(summ(a=15, b=65))
# print(summ(a="Salam", b=65))



