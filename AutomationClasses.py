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
            EC.visibility_of_element_located((By.ID, "our_products"))
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
        self.implicityWaitMainPage()
        categorynames=['speakers','tablets','laptops','mice','headphones']
        if (categoryname not in categorynames):
            raise ValueError("Invalid category name.")
        self.driver.find_element_by_id(f'{categoryname}Img').click()
    def implicityWaitMainPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "our_products"))
        )

    """-----------------------------------------------------------------------------------------------------------------
                                        Cart in the top right functions
    --------------------------------------------------------------------------------------------------------------------"""
    #Get the amount of the products in the cart-top right
    def cartAmount(self):
        return self.driver.find_element_by_xpath("//a[@id='shoppingCartLink']/span[@class='cart ng-binding']").text
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
        for i in range(len(elements)-2):
                self.listOfProducts.append([0,0,0,0])
        for i in range (len(elements)-2):
                for j in range (4):
                    if(j==0):
                        self.listOfProducts[i][j]=self.driver.find_element_by_xpath(f'//li//table[@ng-show="cart.productsInCart.length > 0"]//tr[{i+1}]//h3[@class="ng-binding"]').text
                    if(j==1):
                        self.listOfProducts[i][j] = int(self.driver.find_element_by_xpath(f'//li//table[@ng-show="cart.productsInCart.length > 0"]//tr[{i+1}]//label[@class="ng-binding"]').text.split()[1])
                    if(j==2):
                        price= self.driver.find_element_by_xpath(f'//li//table[@ng-show="cart.productsInCart.length > 0"]//tr[{i+1}]//p[@class="price roboto-regular ng-binding"]').text[1:]
                        if(len(price)==8):#Assuming that the most expensive product is max 9,999.99$
                            price=price[:1]+price[2:]
                        self.listOfProducts[i][j] =float(price)
                    if(j == 3):
                        self.listOfProducts[i][j] = self.driver.find_element_by_xpath(f'//li//table[@ng-show="cart.productsInCart.length > 0"]//tr[{i+1}]//span[@class="ng-binding"]').text
        return self.listOfProducts
    # Comparing the products in the cart to the products you've entered
    def cartCompare(self,products):
        self.getProductDetails()
        self.cartWait()
        self.FIFO()
        for i in range(len(self.listOfProducts)):
            self.listOfProducts[i][0] = self.listOfProducts[i][0][0:len(self.listOfProducts[i][0]) - 3]
            for j in range (4):
                if(j==0):
                    if(self.listOfProducts[i][j] not in products[i][j]):
                        return False
                else:
                    if (self.listOfProducts[i][j] != products[i][j]):
                        return False
        return True
    #Waiting until the cart in the top right is opened
    def cartWait(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//li//table[@ng-show='cart.productsInCart.length > 0']"))
        )
    #clicking the Cart Icon
    def cartClick(self):
        self.driver.find_element_by_id("menuCart").click()
    #Removing products from the cart
    def cartRemove(self,location=1):
        listOfProducts=self.getProductDetails()
        self.driver.find_elements_by_xpath("//div[@class='removeProduct iconCss iconX']")[location].click()
        return listOfProducts[location]
    # Returns if product is in cart
    # You must Create the product details list before starting this function
    def isInCart(self,product):
        return (product in self.listOfProducts)
    #"Rotating" the cart list
    def FIFO(self):
        newList=[]
        for i in range(len(self.listOfProducts)-1,-1,-1):
            newList.append((self.listOfProducts[i]))
        self.listOfProducts=newList


#Category page class
class categoryPage:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
        self.implicityWaitCategoryPage()
    #Open random product page, first chceck if the number is not in the list
    def openRandomProduct(self,ListOfLoc):
        self.implicityWaitCategoryPage()
        products=self.driver.find_elements_by_xpath("//img[@class='imgProduct']")
        location=random.randint(0,len(products)-1)
        while (location in ListOfLoc):
            location = random.randint(0, len(products) - 1)
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
        price= self.driver.find_element_by_xpath("//h2[@class='roboto-thin screen768 ng-binding']").text[1:]
        if (len(price) == 8):  # Assuming that the most expensive product is max 9,999.99$
            price = price[:1] + price[2:]
        productDetails[2] =float(price)
        productDetails[3] = self.driver.find_element_by_xpath("//span[contains(@class,'colorSelected')]").get_attribute('title')
        return productDetails
    #Set the quatity of the product to the given quantity
    def addQuantity(self,quantity):
        for i in range(quantity-1):
            self.driver.find_element_by_xpath("//div[@class='plus']").click()
    #Click on the ADD TO CART button
    def addToCart(self):
        self.driver.find_element_by_name("save_to_cart").click()
    #Add new product to the cart by quantity
    #Returns the product details
    def addNewProduct(self,quantity):
        self.implicityWaitProductPage()
        self.addQuantity(quantity)
        details=self.getProductDetails()
        details[1]=quantity
        details[2]=details[2]*quantity
        self.addToCart()
        return details
    #Wait for the page to load.
    def implicityWaitProductPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Description"))
        )




