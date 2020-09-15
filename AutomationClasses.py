from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from unittest import TestCase
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect
#Login and Logout processes
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
        self.signInButton()
    # Insert username details
    def insertDetails(self):
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.password)
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
    def signInButton(self):
        self.driver.find_element_by_id("sign_in_btnundefined").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='hi-user containMiniTitle ng-binding']"))
        )
    #Log Out process
    def LogOut(self):
        self.personClick()
        self.signOutClick()
    #Waiting for the sign out button
    def waitLogOut(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//label[@ng-click='signOut($event)']"))
        )
    #Click on the sign out button, wait for the sign out
    def signOutClick(self):
        self.driver.find_element_by_xpath("//label[@ng-click='signOut($event)']").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='hi-user containMiniTitle ng-binding ng-hide']"))
        )
#Main page class
class MainPage:
    # Constructor
    def __init__(self, driver):
        self.driver = driver
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element((By.CLASS_NAME, "loader"))
        )
    #Enter the given category page
    """With lower case!"""
    def enterCategoryPage(self,categoryname):
        categorynames=['speakers','tablets','laptops','mice','headphones']
        if (categoryname not in categorynames):
            raise ValueError("Invalid category name.")
        self.driver.find_element_by_id(f'{categoryname}Img').click()
    #Get the amount of the products in the cart-top right
    def cartAmount(self):
        return self.driver.find_element_by_class_name("cart ng-binding")
    #get the elements of the cart in the top right
    def getCartElements(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//li//table[@ng-show='cart.productsInCart.length > 0']"))
        )
        return self.driver.find_elements_by_xpath("//li//table[@ng-show='cart.productsInCart.length > 0']//tr")
    #Get the products details-top right
    #Returns list-it's length- the amount of the carts
    #in each cell in the list- the prodcut details order by:
    #Name[0], Quantity[1], Price[2], Color[3]
    def getProductDetails(self):
        elements=self.getCartElements()
        listOfProducts=[]
        fob nr i in range(len(elements)):
            if(i==0):
                listOfProducts=[[,,,]]
        for i in range (len(elements)):
            if(i<(len(elements)-2)):
                elements[i]=
            else:
                break
#Category page class
class CategoryPage:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "cell categoryRight"))
        )



