import datetime
import json
import sqlite3

import pandas

from app.database.queries import *
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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def tax_info_factory():
    return lambda cursor, row: TaxRow(row[0], row[1], row[2], row[3], row[4])


class IncomeData:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.__init_table()

    @transaction
    def __init_table(self, cursor):
        cursor.execute(CREATE_TAX_INFO_TABLE)

    @transaction
    def find_all(self, cursor):
        cursor.row_factory = tax_info_factory()
        response = pandas.read_sql_query(FIND_ALL_TAX_INFO, self.connection)
        result = list()
        for row in map(lambda row: TaxRow(row[0], row[1], row[2], row[3], row[4]), response.values.tolist()):
            result.append(row)
        return result

    @transaction
    def find_by_dates(self, cursor, from_date, to_date):
        cursor.row_factory = tax_info_factory()
        return cursor.execute(FIND_INCOME_DATA_BETWEEN_DATES, (from_date, to_date)).fetchall()

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
