from datetime import datetime

import centrobank
import data_import
from tax_info import TaxInfo, NewTaxRow
from utils import round_up, repeat_on_invalid_input

DEFAULT_SOURCE_PATH = "source.txt"


@repeat_on_invalid_input
def add_income():
    date = datetime.strptime(input("Enter the date of income with format 'yyyy-MM-dd'\n"), "%Y-%m-%d").date()
    income_val = float(input("Enter the income value \n"))
    try:
        exchange_rate = centrobank.get_exchange_rate(date)
    except:
        exchange_rate = input('Print get info from central bank. Please, enter it manually or change the date \n')
    new_row = NewTaxRow(income_value=income_val, income_date=date, exchange_rate=exchange_rate)
    row = TaxInfo().insert_row(new_row)
    print(f"Tax info added: \n {row}")


def find_annual_income():
    current_year = datetime.now().year
    year = int(input(f"Enter the desired year (def {current_year})\n") or current_year)
    result = count_income({"year": year})
    print(f"The annual income for {year}'s year is {result}")


def count_income(date: dict):
    info = TaxInfo()
    result = 0
    for row in map(lambda x: x.income_value, info.find_by_date(date)):
        result += row
    return result


def find_month_income():
    current_year = datetime.now().year
    current_month = datetime.now().month
    year = int(input(f"Enter the desired year (def {current_year})\n" or current_year))
    month = int(input(f"Enter the desired month def {current_month}\n" or current_month))
    result = count_income({"year": year, "month": month})
    print(f"The annual income for {month}.{year}'s month is {result}")


@repeat_on_invalid_input
def moth_tax_value():
    year = int(input("Enter the desired year \n"))
    month = int(input("Enter the desired month \n"))
    info = TaxInfo()
    result = 0
    for income in map(converted_income(), info.find_by_date({"year": year, "month": month})):
        result += income
    print(f"For  {month}.{year} you should pay {round_up(result * 0.01)}")


def converted_income():
    return lambda x: x.income_value * x.exchange_rate


def import_data():
    try:
        source_file_path = input(f"Enter the source file path (def {DEFAULT_SOURCE_PATH}\n) " or DEFAULT_SOURCE_PATH)
        data_import.import_txt(source_file_path)
    except FileNotFoundError:
        if input("File by path {source_file_path} not found. Would you like to try again? Y/N \n") == 'Y':
            import_data()
