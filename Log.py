from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from unittest import TestCase
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect
class Log:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element((By.CLASS_NAME, "loader"))
        )
    #Log in details
    def LogInDetails(self,username,password):
        self.username=username
        self.password=password
    #Log In process
    def LogIn(self):
        self.personClick()
        self.insertDetails()
    # Insert username details
    def insertDetails(self):
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.password)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='hi-user containMiniTitle ng-binding']"))
        )
    # Click on the person emoji
    def personClick(self):
        self.driver.find_element_by_id("menuUserSVGPath").click()
        if(inspect.stack()[1].function=='LogIn'):
            self.waitLogIn()
        else:
            self.waitLogOut()
    #Wait for the log in screen
    def waitLogIn(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
    #Click on the sign in button
    #Log Out process
    def LogOut(self):
        self.personClick()
        self.signOutClick()
    #Waiting for the sign out button
    def waitLogOut(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
    #Click on the sign out button, wait for the sign out
    def signOutClick(self):
        self.driver.find_element_by_xpath("//label[@ng-click='signOut($event)']").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='hi-user containMiniTitle ng-binding ng-hide']"))
        )



