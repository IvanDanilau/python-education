DATABASE_NAME = "taxes.db"

CREATE_TAX_INFO_TABLE = '''CREATE TABLE IF NOT EXISTS tax_info(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incoming_date TEXT,
    income_value REAL, 
    exchange_rate REAL,
    converted_income_value INT)'''

ADD_TAX_INFO_ROW = '''INSERT INTO tax_info (incoming_date,
income_value,
exchange_rate,
converted_income_value) values (?, ?, ?, ?)
RETURNING *
'''

FIND_ALL_TAX_INFO = 'SELECT * FROM tax_info order by date(incoming_date) desc'

DELETE_ALL_TAX_INFO_ROWS = 'DELETE FROM tax_info'

FIND_TAX_ROW_BY_DATE = '''SELECT * FROM tax_info
                where strftime('%Y', incoming_date) = coalesce(?, strftime('%Y', incoming_date))
                and strftime('%m', incoming_date) = coalesce(?, strftime('%m', incoming_date))
                and strftime('%d', incoming_date) = coalesce(?, strftime('%d', incoming_date))'''
