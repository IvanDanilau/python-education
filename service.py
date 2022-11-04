from tax_info import TaxInfo
from utils import round_up


def find_annual_income():
    try:
        year = int(input("Enter the desired year \n"))
        info = TaxInfo()
        result = 0
        for row in map(lambda x: x.income_value, info.findByDate({"year": year})):
            result += row
        print(f"The annual income for {year}'s year is {result}")
    except ValueError:
        if input("Try again? Y/N \n") == 'Y':
            find_annual_income()


def moth_tax_value():
    try:
        year = int(input("Enter the desired year \n"))
        month = int(input("Enter the desired month \n"))
        info = TaxInfo()
        result = 0
        for income in map(converted_income(), info.findByDate({"year": year, "month": month})):
            result += income
        print(f"For  {month}.{year} you should pay {round_up(result * 0.01)}")
    except ValueError:
        if input("Try again? Y/N \n") == 'Y':
            moth_tax_value()


def converted_income():
    return lambda x: x.income_value * x.exchange_rate
