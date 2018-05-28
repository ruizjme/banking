#!/Users/Jaime/anaconda3/bin/python

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import getpass
import os.path
import csv

def load_all_items(driver):
	'''
	Scroll down all the way in order to load all the items in the category.
	'''

	time.sleep(1)

	SCROLL_PAUSE_TIME = 1

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


def sign_in(driver, user, loginURL, errorURL=False):

	driver.get(loginURL)

	print('Attempting login')
	driver.find_element_by_name('userid').send_keys(user)
	passwd = getpass.getpass('Password: ')
	driver.find_element_by_name('password').send_keys(passwd, Keys.ENTER)
	del passwd

	print('Logging in...')

	time.sleep(1)

	# TODO: fix wrong pw retry block
	if errorURL:
		while driver.current_url == errorURL:
			print('Wrong password')
			print('Try again')
			driver.find_element_by_id('username').send_keys(user)
			passwd = getpass.getpass('Password: ')
			driver.find_element_by_id('password').send_keys(passwd, Keys.ENTER)
			del passwd
			print('Logging in...')

			time.sleep(1)

def filter_transactions(driver, period=90):
	driver.find_element_by_xpath('//*[@id="transactions"]/app-component/ib-transactions/div/div/div/ib-filter/div/form/div/div[1]/div/div[2]/div[2]/button').click()
	driver.find_element_by_xpath('//*[@id="input-transaction-period"]/a/span[2]/div').click()

	if period == 90:
		pass
		# TODO: finish this


def download_transactions(driver):

	print('Finding transactions...')
	driver.get('https://ib.nab.com.au/nabib/transactionHistorySelectAccount.ctl#/transactions')
	# time.sleep(1)


	driver.find_element_by_xpath('//*[@id="accountSelect"]').click()
	time.sleep(1)

	# TODO: add if statement to choose account from parameters passed
	jointAcct = '//*[@id="ui-select-choices-row-0-0"]/div/div/ib-ui-select-choices/div/div[2]'
	transactionAcct = '//*[@id="ui-select-choices-row-0-1"]/div/div/ib-ui-select-choices/div'
	savingsAcct = '//*[@id="ui-select-choices-row-0-2"]/div/div/ib-ui-select-choices/div'

	driver.find_element_by_xpath(jointAcct).click()
	time.sleep(1)

	# TODO: change number of transactions to maximum or last year or whatever
	driver.find_element_by_xpath('//*[@id="exportTransactionsBtn"]').click()
	print('Downloading transactions...')


# def extract_transactions():
# 	filePath = '/Users/Jaime/Downloads/TransactionHistory.csv'
# 	while not os.path.exists(filePath):
# 		print("waiting for download to finish")
# 		time.sleep(1)
# 	with open(filePath) as f:
# 		reader = csv.reader(f)
# 		for row in reader:
# 			print('{:<9} {:>9}  {}'.format(row[0], row[1], row[5]))
# 	os.remove(filePath)
