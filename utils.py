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


def round_up(num: float):
    """custom summary rounding """
    val = num * 1000 % 1000
    return math.ceil(num) if val >= 445 else math.floor(num)
