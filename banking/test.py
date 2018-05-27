#!/Users/Jaime/anaconda3/bin/python

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def worksheet(sheet_name):

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open(sheet_name).sheet1
    return wks





wks = worksheet('API Test')

wks.update_acell('B2', "Helena is wacky.")

# Fetch a cell range
cell_list = wks.range('A1:B7')

print(cell_list)
