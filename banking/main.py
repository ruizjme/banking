#!/usr/bin/python
from __future__ import print_function
import time
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
# import getpass
import os.path
import csv
import json
import re
# from apiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools

# custom modules in this directory
import nab
import sheets

time0 = time.time()

with open('./.USER-DATA', 'r') as f:
	data = json.load(f)
	user = data['user']

nab.sign_in(user)
nab.download_transactions()

filePath = '/Users/Jaime/Downloads/TransactionHistory.csv'
while not os.path.exists(filePath):
	print("waiting for download to finish")
	time.sleep(1)

nab.quit()

rows = []
pat1 = re.compile(r'(V\d{4}) (\d\d/\d\d) ([\w\s]+) (\d+)')
with open(filePath) as f:
	reader = csv.reader(f)
	for row in reader:
		m = pat1.match(row[5])
		if m is not None:
			card = re.sub(r'\s+',' ',m.group(1).strip())
			date = row[0]# OR re.sub(r'\s+',' ',m.group(2).strip())
			amount = row[1]
			transaction_type = row[4]
			description = re.sub(r'\s+',' ',m.group(3).strip())
			number = re.sub(r'\s+',' ',m.group(4).strip())

			rows.append([date, amount, card, description, transaction_type, number])
		else:
			pass # deal with other format transactions



service = sheets.setup()

# Call the Sheets API
SPREADSHEET_ID = '1XCtBEwkNBwKPZMphSFWvffTnGVRxwVkFycbcFC2mscc'
RANGE_NAME = 'Sheet1!A:G'

body = {'values': rows}
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
	range=RANGE_NAME, body=body, valueInputOption='RAW'
	).execute()

print('{0} cells updated.'.format(result.get('updatedCells')))



############ WIP: add amounts for certain categories
coles = 0
for row in rows:
	if 'coles' in row[3].lower():
		coles += float(row[1])

print('Spent at Coles in the last 30 days (test):', coles)



print('Total time: {} s'.format(time.time() - time0))
