from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from unittest import TestCase
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect
path = r"C:\Driver\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://www.advantageonlineshopping.com/#/")
driver.find_element_by_id("17").send_keys()
