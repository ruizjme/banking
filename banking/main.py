#!/usr/bin/python
from __future__ import print_function
import time
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
# import getpass
import os.path
import csv
import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import nab

time0 = time.time()
# driver = webdriver.Chrome()
# driver.implicitly_wait(10)
# print('Loading Internet Banking...')

# with open('./.USER-DATA', 'r') as userData:
	# user = userData.read().strip('\n')

# loginURL = 'https://ib.nab.com.au/nabib/login.ctl'
# errorURL = loginURL+'?error=201001'
# sign_in(driver, user, loginURL, errorURL)
# download_transactions(driver)

card_holders = {'V0133':'Jaime',
				'V8479':'Helena',
				'V3608':'Jaime-old'	}

rows = []
pat1 = re.compile(r'(V\d{4}) (\d\d/\d\d) ([\w\s]+) (\d+)')
filePath = '/Users/Jaime/Downloads/TransactionHistory.csv'
while not os.path.exists(filePath):
	print("waiting for download to finish")
	time.sleep(1)
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

# os.remove(filePath)





# Setup the Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
SPREADSHEET_ID = '1XCtBEwkNBwKPZMphSFWvffTnGVRxwVkFycbcFC2mscc'
RANGE_NAME = 'Sheet1!A:G'

body = {'values': rows}
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
	range=RANGE_NAME, body=body, valueInputOption='RAW'
	).execute()
print('{0} cells updated.'.format(result.get('updatedCells')))

# driver.quit()
print('Total time: {} s'.format(time.time() - time0))
