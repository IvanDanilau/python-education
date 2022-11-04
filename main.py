# This is a sample Python script.
import service


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
def menu_description():
    return '''
*****************************     
    We have next commands:
 - AI - get annual income
 - MT - get month tax value
 - exit - exit the program
*****************************
 '''


if __name__ == '__main__':
    # storage = TaxInfo("taxes.db")
    # tax_row = TaxRow(1233, datetime(2022, 11, 12), 2.4347)
    # storage.insert_row(tax_row)
    # date = datetime.strptime('2022 10 1', '%Y %m %d')
    # storage.findByDate(date)
    # storage.findAll()
    print(" Greetings!")
    while True:
        val = input(menu_description())

        if val == 'exit':
            print("Have a good day!")
            break
        if val == 'AI':
            service.find_annual_income()
            continue
        if val == 'MT':
            service.moth_tax_value()
            continue
        else:
            print("Unrecognized command. Try again")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
