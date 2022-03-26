import nextcord
import constants
from pymongo import MongoClient
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def getNumMembers(client):
    membersz=0
    for x in client.guilds:
        membersz+=len(x.members)+1
    return membersz

async def updatePresence(client):
    await client.change_presence(
        status=nextcord.Status.online, 
        activity=nextcord.Game(
            name = "%shelp %s users"%(
                constants.CMD_PREFIX, getNumMembers(client)
                )
            )
        )


def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"```{cmd_and_aliases} {params}```"


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