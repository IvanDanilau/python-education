from datetime import datetime

from app.database.tax_info import IncomeData, NewTaxRow
from app.service import centrobank, data_import

DEFAULT_SOURCE_PATH = "../../source.txt"


def find_income_info(from_date=None, to_date=None):
    income_data = IncomeData()
    return income_data.find_by_dates(from_date, to_date)


def add_income_info(income_value, income_date):
    date = datetime.strptime(income_date, "%Y-%m-%d").date()
    income_val = float(income_value)
    # FIXME actualize it
    try:
        exchange_rate = centrobank.get_exchange_rate(date)
    except:
        exchange_rate = input('Print get info from central bank. Please, enter it manually or change the date \n')
    new_row = NewTaxRow(income_value=income_val, income_date=date, exchange_rate=exchange_rate)
    row = IncomeData().insert_row(new_row)
    return row


def get_income_value(from_date=None, to_date=None, converted=True):
    if type(converted == str) and converted.lower() == 'false':
        converted = False
    if from_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    if to_date:
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
    if converted:
        func = lambda x: x.converted_income_value
    else:
        func = lambda x: x.income_value
    total = 0
    for inc_value in map(func, find_income_info(from_date, to_date)):
        total += inc_value
    return total


def import_data():
    try:
        source_file_path = input(f"Enter the source file path (def {DEFAULT_SOURCE_PATH}) \n") or DEFAULT_SOURCE_PATH
        data_import.import_txt(source_file_path)
    except FileNotFoundError:
        if input("File by path {source_file_path} not found. Would you like to try again? Y/N \n") == 'Y':
            import_data()
