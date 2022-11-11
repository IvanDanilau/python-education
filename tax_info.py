import datetime
import sqlite3

from queries import *
from utils import *


class NewTaxRow:

    def __init__(self, income_value: float, income_date: datetime, exchange_rate: float):
        self.id = id
        self.income_value = income_value
        self.income_date = income_date
        self.exchange_rate = exchange_rate

    def to_tuple(self):
        if self.income_date and self.income_value and self.exchange_rate:
            converted_income_value = round_up(self.income_value * self.exchange_rate)
            return str(self.income_date), self.income_value, self.exchange_rate, converted_income_value
        else:
            raise Exception("invalid row")


class TaxRow:
    def __init__(self, id, income_date, income_value, exchange_rate, converted_income_value):
        self.id = id
        self.income_date = income_date
        self.income_value = income_value
        self.exchange_rate = exchange_rate
        self.converted_income_value = converted_income_value

    def __str__(self) -> str:
        return f"""" Tax row info : \n
    - income value in USD {self.income_value} \n
    - income date {self.income_date} \n
    - exchange rate {self.exchange_rate} \n
    - income value in GEL {self.converted_income_value} \n
               """


def tax_info_factory():
    return lambda cursor, row: TaxRow(row[0], row[1], row[2], row[3], row[4])


class TaxInfo:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.__init_table()

    @transaction
    def __init_table(self, cursor):
        cursor.execute(CREATE_TAX_INFO_TABLE)

    @transaction
    def find_all(self, cursor):
        for row in cursor.execute(FIND_ALL_TAX_INFO):
            print(row)

    @transaction
    def find_by_date(self, cursor, date: dict):
        year = None if date.get("year") is None else str(date.get('year'))
        month = None if date.get("month") is None else str(date.get('month'))
        day = None if date.get("day") is None else str(date.get('day'))
        cursor.row_factory = tax_info_factory()
        return cursor.execute(FIND_TAX_ROW_BY_DATE, (year, month, day)).fetchall()

    @transaction
    def insert_row(self, cursor, value: NewTaxRow) -> TaxRow:
        existed = self.find_existed(cursor, value)
        if not existed:
            cursor.row_factory = tax_info_factory()
            return cursor.execute(ADD_TAX_INFO_ROW, value.to_tuple()).fetchone()
        else:
            print("income info already exists, returning existed")
            return existed

    def find_existed(self, cursor, value):
        cursor.row_factory = tax_info_factory()
        return cursor.execute(FIND_TAX_ROW_BY_DATE_AND_INC_VALUE, (value.income_date, value.income_value)) \
            .fetchone()

    def __del__(self):
        self.connection.close()
