import math


def transaction(func):
    """Decorator for transactions"""

    def wrapper(*args):
        database = args[0]
        cursor = database.connection.cursor()
        if len(args) > 1:
            result = func(database, cursor, *args[1:])
        else:
            result = func(database, cursor)
        database.connection.commit()
        return result

    return wrapper


def repeat_on_invalid_input(func):
    """
    Useful for functions, which expect user input values
    If user input unexpected value, he could try input it again
    """

    def wrapper(*args):
        try:
            return func(*args)
        except ValueError:
            if input("Invalid input data. Would you like to try again? Y/N \n") == 'Y':
                wrapper(*args)

    return wrapper


def round_up(num: float):
    """
    custom summary rounding
    takes 3 digits after the decimal point and round it in ceil, couse it's better to pay
     a little more, then have any debt
    """
    val = num * 1000 % 1000
    return math.ceil(num) if val >= 445 else math.floor(num)
