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
    #LIFO- Last In First Out
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
        self.driver.find_element_by_id("menuCart").click()
    #Removing products from the cart
    def cartRemove(self,location):
        listOfProducts=self.getProductDetails()
        self.driver.find_elements_by_xpath("//div[@class='removeProduct iconCss iconX']")[location].click()
        return listOfProducts[location]
    # Returns if product is in cart
    # You must Create the product details list before starting this function
    def isInCart(self,product):
        return (product in self.listOfProducts)
#Category page class
class categoryPage:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
        self.implicityWaitCategoryPage()
    #Open random product page, first chceck if the number is not in the list
    def openRandomProduct(self,ListOfLoc=None):
        self.implicityWaitCategoryPage()
        products=self.driver.find_elements_by_xpath("//img[@class='imgProduct']")
        location=random.randint(0,len(products)-1)
        if(ListOfLoc==None):
            ListOfLoc=[]
        while (location not in ListOfLoc):
            location = random.randint(0, len(products) - 1)
            if(location not in ListOfLoc):
                ListOfLoc.append((location))
        products[location].click()
        ListOfLoc.append(location)
        return ListOfLoc
    # Wait for the page to load.
    def implicityWaitCategoryPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='cell categoryRight']"))
        )
    #Click on the back button wand wait for the page to load/
    def backAndWait(self):
        self.driver.back()
        self.implicityWaitCategoryPage()
#Product page class
class productPage:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
    # Get the products details-top right
    # Returns list-it's length- the amount of the carts
    # in each cell in the list- the prodcut details order by:
    # Name[0], Quantity[1]=0-Cant Reach, Price[2], Color[3]
    def getProductDetails(self):
        productDetails=[0,0,0,0]
        productDetails[0]=self.driver.find_element_by_xpath("//h1[@class='roboto-regular screen768 ng-binding']").text
        productDetails[2] = self.driver.find_element_by_xpath("//h2[@class='roboto-thin screen768 ng-binding']").text
        productDetails[3] = self.driver.find_element_by_xpath("//span[@data-ng-repeat='color in colors']").get_attribute('title')
        return productDetails
    #Set the quatity of the product to the given quantity
    def addQuantity(self,quantity):
        for i in range(quantity-1):
            self.driver.find_element_by_xpath("//div[@class='plus']").click()
    #Click on the ADD TO CART button
    def addToCart(self):
        self.driver.find_element_by_nam("save_to_cart").click()
    #Add new product to the cart by quantity
    #Returns the product details
    def addNewProduct(self,quantity):
        self.implicityWaitProductPage()
        details=self.getProductDetails()
        details[1]=quantity
        self.addQuantity(quantity)
        self.addToCart()
    #Wait for the page to load.
    def implicityWaitProductPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Description"))
        )




