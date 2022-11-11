# This is a sample Python script.
import service


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
def menu_description():
    return '''
*****************************     
    We have next commands:
 - 'add inc' - add income information
 - 'imp data' - import tax data from txt file 
 - 'annual inc' - get annual income
 - 'month inc' - get month income
 - 'month tax' - get month tax value
 - 'exit' - exit the program
*****************************
 '''


if __name__ == '__main__':
    print(" Greetings!")
    while True:
        val = input(menu_description()).replace(" ", "").lower()
        if val == 'exit':
            print("Have a good day!")
            break
        if val == 'annualinc':
            service.find_annual_income()
            continue
        if val == 'monthinc':
            service.find_month_income()
            continue
        if val == 'monthtax':
            service.moth_tax_value()
            continue
        if val == "addinc":
            service.add_income()
        if val == "impdata":
            service.import_data()
            continue
        else:
            print("Unrecognized command. Try again")
