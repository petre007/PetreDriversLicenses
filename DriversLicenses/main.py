import requests
import json
import datetime
import pandas as pd

url = "http://localhost:30000/drivers-licenses/list"


class Operations:
    def __init__(self, data):
        self.data = data

    def populateData(self):
        if len(self.data) == 0:
            while len(self.data) < 150:
                response_json = requests.get(url)
                data_arr = json.loads(response_json.text)
                self.data.extend(data_arr)

    def listOfSuspendedLicenses(self):
        suspendedLicenses = []
        for dt in self.data:
            if dt['suspendat']:
                suspendedLicenses.append(dt)
        df = pd.DataFrame.from_dict(suspendedLicenses)
        df.to_excel('suspended_licenses.xlsx')

    def listOfValidLicenses(self):
        today = datetime.datetime.now()
        validLicenses = []
        for dt in self.data:
            datetimeLicense = datetime.datetime.strptime(dt['dataDeExpirare'], "%d/%m/%Y")
            if datetimeLicense.date() > today.date():
                validLicenses.append(dt)
        df = pd.DataFrame.from_dict(validLicenses)
        df.to_excel('valid_licenses.xlsx')

    def listOfLicensesBasedOnCategoryAndTheirCount(self):
        df = pd.DataFrame(self.data)
        listOfLicenses = df.groupby(['categorie'])['categorie'].count()
        listOfLicenses.to_excel('list_of_licenses_based_on_the_category_and_count.xlsx')


def main():
    data = Operations([])
    print("Loading data...")
    data.populateData()
    print("Data has been successfully loaded.")
    print("Welcome to driver licenses department!\n"
          "Type the number of operation you want to execute:\n"
          "1 -> get the list of suspended drivers\n"
          "2 -> get the list of valid licenses\n"
          "3 - > get the list of licenses based on their category and their count\n"
          "-1 -> exit the program\n"
          "Note: the data is saved on .xlsx file")
    data.listOfLicensesBasedOnCategoryAndTheirCount()
    operation = -2
    while int(operation) != -1:
        operation = input("Enter operation: ")
        if int(operation) == 1:
            data.listOfValidLicenses()
            print("Valid licenses list have been saved.")
        if int(operation) == 2:
            data.listOfSuspendedLicenses()
            print("Suspended licenses list have been saved")
        if int(operation) == 3:
            data.listOfLicensesBasedOnCategoryAndTheirCount()
            print("List of licenses group by their category and count has been saved")
        if int(operation) == -1:
            print("Exiting the program...")
            break


if __name__ == "__main__":
    main()
