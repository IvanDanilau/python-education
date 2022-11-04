import datetime
import sqlite3

from queries import *
from utils import *


class TaxRow:

    def __init__(self, income_value: int, income_date: datetime, exchange_rate: float):
        self.income_value = income_value
        self.income_date = income_date
        self.exchange_rate = exchange_rate

    def toTuple(self):
        if self.income_date and self.income_value and self.exchange_rate:
            converted_income_value = round_up(self.income_value * self.exchange_rate)
            return str(self.income_date), self.income_value, self.exchange_rate, converted_income_value
        else:
            raise Exception("invalid row")


def tax_info_factory():
    return lambda cursor, row: TaxRow(row[2], row[1], row[3])


class TaxInfo:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.__init_table()

    @transaction
    def __init_table(self, cursor):
        cursor.execute(CREATE_TAX_INFO_TABLE)

    @transaction
    def findAll(self, cursor):
        for row in cursor.execute(FIND_ALL_TAX_INFO):
            print(row)

    @transaction
    def findByDate(self, cursor, date: dict):
        year = None if date.get("year") is None else str(date.get('year'))
        month = None if date.get("month") is None else str(date.get('month'))
        day = None if date.get("day") is None else str(date.get('day'))
        cursor.row_factory = tax_info_factory()
        return cursor.execute(FIND_TAX_ROW_BY_DATE, (year, month, day)).fetchall()

    @transaction
    def insert_row(self, cursor, value: TaxRow):
        cursor.execute(ADD_TAX_INFO_ROW, value.toTuple())

    @transaction
    def clear_data(self, cursor):
        cursor.execute(DELETE_ALL_TAX_INFO_ROWS)

    def __del__(self):
        self.connection.close()
