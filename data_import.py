from datetime import datetime

import centrobank
from tax_info import NewTaxRow, TaxInfo


def import_txt(source_file_path):
    try:
        with open(source_file_path) as source:
            headers = list(source.readline().strip().split(" "))
            date_inc_idx = headers.index("date_income")
            inc_val_idx = headers.index("incoming_value")
            new_rows = []
            invalid_rows = 0
            for row in source.readlines():
                new_row = __map_to_nex_tax_row(date_inc_idx, inc_val_idx, row)
                if new_row is None:
                    invalid_rows += 1
                else:
                    new_rows.append(new_row)
            if len(new_rows):
                info = TaxInfo()
                for row in new_rows:
                    info.insert_row(row)
            print(f"Valid rows count {len(new_rows)} imported")
            print(f"Invalid rows count {invalid_rows}")
    except ValueError:
        print("Could not declare required table params : 'date_income' & 'incoming_value'")


def __map_to_nex_tax_row(date_inc_idx, inc_val_idx, row):
    try:
        values = row.strip().split(" ")
        date_income = datetime.strptime(values[date_inc_idx], "%Y-%m-%d")
        income_value = float(values[inc_val_idx])
        exchange_rate = centrobank.get_exchange_rate(date_income)
        return NewTaxRow(income_value, date_income, exchange_rate)
    except ValueError:
        print(f"Invalid row data: '{row}'")
        return None
