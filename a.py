from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from unittest import TestCase
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect
import time
path = r"C:\Driver\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://www.advantageonlineshopping.com/#/")
time.sleep(5)
driver.get("https://www.w3schools.com/python/ref_func_map.asp")
time.sleep(5)
driver.back()
driver.find_element_by_id("17").send_keys()
driver.find_element_by_xpath("aa").get_attribute('asd')
