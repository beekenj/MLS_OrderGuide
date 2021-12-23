#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os
import json

def get_shamrock():

    init_str = '''

    Connecting to Shamrock

    '''

    success_str = '''

    Shamrock: connection successful

    '''

    failure_str = '''

    Shamrock: chromedriver exception

    '''

    print(init_str)

    url = 'https://www.shamrockorders.com/Catalog'
    user_input = '//*[@id="UserName"]'
    password_input = '//*[@id="Password"]'
    signin_button = '//*[@id="bottom-section-buttons"]/input'
    inv_man_button = '/html/body/div[1]/div/ul/li[5]/a/span'
    order_guides_tab = '//*[@id="contractOrderGuide"]'
    guide_menu_button = '//*[@id="0300114146"]/td[4]/div/div[1]/a/span/i'
    export_button = '//*[@id="0300114146"]/td[4]/div/div[1]/ul/li[2]'
    csv_button = '//*[@id="ToolTables_soe-table-product_0"]'

    WINDOW_SIZE = "1920,1080"

    p = {"download.default_directory":os.getcwd()+'/PriceLists'}

    keys = json.load(open('./.app_info/keys.json'))['shamrock']

    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    
    ## Experimental
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")



    chrome_options.add_experimental_option("prefs",p)

    serv = Service(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=serv, options=chrome_options)

    try:
        driver.get(url)

        driver.find_element(By.XPATH, user_input).send_keys(keys['email'])
        driver.find_element(By.XPATH, password_input).send_keys(keys['password'])
        driver.find_element(By.XPATH, signin_button).click()

        driver.find_element(By.XPATH, inv_man_button).click()
        time.sleep(10)
        driver.find_element(By.XPATH, order_guides_tab).click()
        time.sleep(5)
        driver.find_element(By.XPATH, guide_menu_button).click()
        time.sleep(5)
        driver.find_element(By.XPATH, export_button).click()
        time.sleep(5)
        driver.find_element(By.XPATH, csv_button).click()

        time.sleep(5)
        driver.quit()

        print(success_str)
        return True
    except:
        print(success_str)
        return False


def rename_shamrock():
    # Rename downloaded file
    files = os.listdir('./PriceLists')
    match = [x for x in files if re.search('OrderGuide', x)]
    if len(match) > 0:
        os.rename('./PriceLists/' + match[0], './PriceLists/Shamrock.csv')
