from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from unittest import TestCase
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect
import random
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
    #With lower case!
    def enterCategoryPage(self,categoryname):
        categorynames=['speakers','tablets','laptops','mice','headphones']
        if (categoryname not in categorynames):
            raise ValueError("Invalid category name.")
        self.driver.find_element_by_id(f'{categoryname}Img').click()
    """-----------------------------------------------------------------------------------------------------------------
                                        Cart in the top right functions
    --------------------------------------------------------------------------------------------------------------------"""
    #Get the amount of the products in the cart-top right
    def cartAmount(self):
        return self.driver.find_element_by_xpath("//a[@id='shoppingCartLink']/span[@class='cart ng-binding']")
    #get the elements of the cart in the top right
    def getCartElements(self):
        self.cartWait()
        return self.driver.find_elements_by_xpath("//li//table[@ng-show='cart.productsInCart.length > 0']//tr")
    #Get the products details-top right
    #Returns list-it's length- the amount of the carts
    #in each cell in the list- the prodcut details order by:
    #Name[0], Quantity[1], Price[2], Color[3]
    def getProductDetails(self):
        elements=self.getCartElements()
        self.listOfProducts=[]
        for i in range(len(elements)):
                self.listOfProducts.append([0,0,0,0])
        for i in range (len(elements)):
            if(i<(len(elements)-2)):
                for j in range (4):
                    if(j==0):
                        self.listOfProducts[i][j]=elements[i].find_element_by_xpath("//h3[@class='ng-binding']")
                    if(j==1):
                        self.listOfProducts[i][j] = elements[i].find_element_by_xpath("//label[@class='ng-binding']").split()[1]
                    if(j==2):
                        self.listOfProducts[i][j] = elements[i].find_element_by_xpath("//span[@class='ng-binding']")
                    if(j == 3):
                        self.listOfProducts[i][j] = elements[i].find_element_by_xpath("//p[@class='price roboto-regular ng-binding']")
            else:
                break
        print(self.listOfProducts)
        return self.listOfProducts
    # Comparing the products in the cart to the products you've entered
    def cartCompare(self,products):
        for i in range(len(self.listOfProducts)):
            for j in range(4):
                assert products[i][j]==self.listOfProducts[i][j]
    #Waiting until the cart in the top right is opened
    def cartWait(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//li//table[@ng-show='cart.productsInCart.length > 0']"))
        )
    #clicking the Cart Icon
    def cartClick(self):
    #Removing products from the cart
    def cartRemove(self,loctation):
        try:
            self.cartWait()
        except:
            self.

#Category page class
class categoryPage:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "cell categoryRight"))
        )
    #Open random product page
    def openRandomProduct(self):
        products=random.shuffle(self.driver.find_elements_by_xpath("//img[@class='imgProduct']"))
        products[0].click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Description"))
        )
#Product page class
class productPage:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
    # Get the products details-top right
    # Returns list-it's length- the amount of the carts
    # in each cell in the list- the prodcut details order by:
    # Name[0], Quantity[1], Price[2], Color[3]
    def getProductDetails(self):

#



