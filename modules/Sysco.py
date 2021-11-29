#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import re
import os
import json

def get_sysco():

	form_email = '//*[@id="idp-discovery-username"]'
	button_email_submit = '//*[@id="idp-discovery-submit"]'
	form_password = '//*[@id="okta-signin-password"]'
	button_signin = '//*[@id="okta-signin-submit"]'
	form_email2 = '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/input'
	button_email_submit2 = '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div[1]/button'

	list_dropdown = '//*[@id="app"]/div/div[2]/div[1]/div/nav/div[2]/ul/div[3]'
	list_select = '//*[@id="app"]/div/div[2]/div[1]/div/nav/div[2]/ul/div[4]/li[1]/a/div'
	list_menu = '//*[@id="app"]/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/div/div[4]/div/div/div/button/div/div'
	export_button = '//*[@id="app"]/div/div[2]/div[3]/div/div/div/div/div[1]/div[2]/div/div[4]/div/div/div/div/li[2]'
	price_include = '//*[@id="app"]/div/div[10]/div[1]/div/div/div[2]/div[2]/div/div'
	export_button2 = '//*[@id="app"]/div/div[10]/div[1]/div/div/div[3]/button[2]'

	url = 'https://secure.sysco.com/'

	p = {"download.default_directory":os.getcwd()+'/PriceLists'}

	keys = json.load(open('./.app_info/keys.json'))['sysco']

	chrome_options = Options()
	# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
	chrome_options.add_experimental_option("prefs",p)

	serv = Service(executable_path='chrome/chromedriver')

	driver = webdriver.Chrome(service=serv, options=chrome_options)

	try:
		driver.get(url)


		driver.find_element(By.XPATH, form_email).send_keys(keys['email'])

		driver.find_element(By.XPATH, button_email_submit).click()
		time.sleep(2)

		driver.find_element(By.XPATH, form_password).send_keys(keys['password'])
		time.sleep(2)
		driver.find_element(By.XPATH, button_signin).click()
		time.sleep(10)

		driver.find_element(By.XPATH, form_email2).send_keys('mustardsboulder1@gmail.com')
		time.sleep(2)
		driver.find_element(By.XPATH, button_email_submit2).click()
		time.sleep(10)

		# driver.find_element(By.XPATH, list_dropdown).click()
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, list_dropdown))).click()
		time.sleep(5)

		driver.find_element(By.XPATH, list_select).click()
		# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, list_select))).click()
		time.sleep(5)


		driver.find_element(By.XPATH, list_menu).click()
		time.sleep(10)

		driver.find_element(By.XPATH, export_button).click()
		time.sleep(5)

		driver.find_element(By.XPATH, price_include).click()
		time.sleep(5)

		driver.find_element(By.XPATH, export_button2).click()

		time.sleep(5)
		driver.quit()

		print('Sysco: connection successful')
		return True
	except:
		print('Sysco: chromedriver exception')
		return False


def rename_sysco():
	# Rename downloaded file
	files = os.listdir('./PriceLists')
	match = [x for x in files if re.search('Shop_MLS', x)]
	if len(match) > 0:
	    os.rename('./PriceLists/' + match[0], './PriceLists/Sysco.csv')

