import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def getSpreadSheetData(credentials_file : str, spreadSheet_title: str) -> list[dict]:
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)


    # get the instance of the Spreadsheet
    sheet = client.open(spreadSheet_title)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    # get all the records of the data
    records_data = sheet_instance.get_all_records()

    # view the data
    return records_data

def main():
    print("we out")
    content = getSpreadSheetData(r"C:\Users\trexx\Documents\PYTHON CODE LOL\CODEBOZU\bozuBot\credentials.json", "testerData")
    print(content)
    print("done")

if __name__ == "__main__":
    main()