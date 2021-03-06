from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect
import random
from selenium.webdriver.common.action_chains  import ActionChains
#Converting the price from string to float.
def priceToFloat(price):
    price=price.replace(',','')
    price=price.replace('$', '')
    return float(price)
import time
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
    #Implicity wait main page
    def implicityWaitMainPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "our_products")))
    #Returns to main page
    def returnToMainPage(self):
        self.driver.find_element_by_class_name("logo").click()
        self.implicityWaitMainPage()


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
                        price= self.driver.find_element_by_xpath(f'//li//table[@ng-show="cart.productsInCart.length > 0"]//tr[{i+1}]//p[@class="price roboto-regular ng-binding"]').text
                        self.listOfProducts[i][j] =priceToFloat(price)
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
    #Waiting until the cart in the top right is open
    def cartWait(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//li//table[@ng-show='cart.productsInCart.length > 0']")))
    #Clicking the Cart Icon
    def cartClick(self):
        self.driver.find_element_by_id("menuCart").click()
    #Removing product from the cart
    def cartRemove(self,location=0):
        listOfProducts=self.getProductDetails()
        self.driver.find_elements_by_xpath("//div[@class='removeProduct iconCss iconX']")[location].click()
        return listOfProducts[location]
    # Returns if product is in cart
    # You must Create the product details list before starting this function
    def isInCart(self,product):
        self.getProductDetails()
        return (product in self.listOfProducts)
    #"Rotating" the cart list
    def FIFO(self):
        newList=[]
        for i in range(len(self.listOfProducts)-1,-1,-1):
            newList.append((self.listOfProducts[i]))
        self.listOfProducts=newList

#User processes
class User:
    #Constructor
    def __init__(self,driver):
        self.driver=driver

    """-----------------------------------------------------------------------------------------------------------------
                                        Log In/Out functions
    --------------------------------------------------------------------------------------------------------------------"""
    #Log in details
    def LogInDetails(self,username,password):
        self.username=username
        self.password=password
    #Log In process
    def LogIn(self,username,password):
        self.LogInDetails(username,password)
        self.personClick()
        self.insertDetails()
        self.signInButton()
    #Implicity wait main page
    def implicityWaitMainPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "our_products"))
        )
    # Insert username details
    def insertDetails(self):
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.password)
    # Click on the person emoji
    def personClick(self):
        self.driver.find_element_by_id("menuUserSVGPath").click()
        if(inspect.stack()[1].function=='LogIn'):
            self.waitLogIn()
        elif (inspect.stack()[1].function=='LogOut'):
            self.waitLogOut()
        else:
            self.waitAlreadyConnected()
    #Wait for the log in screen
    def waitLogIn(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
    #Click on the sign in button
    def signInButton(self):
        self.driver.find_element_by_id("sign_in_btnundefined").click()
        self.waitSignIn()
    #Implicity wait after signing in
    def waitSignIn(self):
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
    # Click on the sign out button, wait for the sign out
    def signOutClick(self):
        self.driver.find_element_by_xpath("//label[@ng-click='signOut($event)']").click()
    # Implicity wait after signing in
    def waitSignOut(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='hi-user containMiniTitle ng-binding ng-hide']")))


    """-----------------------------------------------------------------------------------------------------------------
                                        Orders functions
    --------------------------------------------------------------------------------------------------------------------"""
    #Implicity wait when you are logged in
    def waitAlreadyConnected(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//header//*[@id='loginMiniTitle']")))
    #Clicking on the my orders button
    def clickMyOrders(self):
        self.driver.find_element_by_xpath("// header // * [ @ translate = 'My_Orders']").click()
        self.waitOrders()
    #Implicity wait for my orders window
    def waitOrders(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "myAccountContainer")))
    #Returns the last order ID
    def __returnLastOrderId(self):
        elements=self.driver.find_elements_by_xpath("//tr[@data-ng-repeat-start='order in myOrdersCtrl.orders track by $index']")
        return elements[len(elements)-1].text.split()[0]
    #Method that returns the last order id
    #This method does the full process
    def getLastOrderId(self):
        self.personClick()
        self.clickMyOrders()
        self.waitOrders()
        return self.__returnLastOrderId()

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
        self.implicityWaitCategoryPage()
        products[location].click()
        return ListOfLoc
    # Wait for the page to load.
    def implicityWaitCategoryPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='cell categoryRight']"))
        )
    #Click on the back button and wait for the page to load
    def backAndWait(self):
        self.driver.back()
        self.implicityWaitCategoryPage()

    #Check if the category title equals the givem title.
    def categoryTitleEqual(self,title):
        self.implicityWaitCategoryPage()
        categoryname = self.driver.find_element_by_xpath('//h3[@class="categoryTitle roboto-regular sticky ng-binding"]').text
        return title == categoryname #Return True or False

#Product page class
class productPage:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
    # Get the products details-top right
    # Returns list-it's length- the amount of the  products in cart
    # in each cell in the list- the prodcut details order by:
    # Name[0], Quantity[1]=0-Cant Reach, Price[2], Color[3]
    def getProductDetails(self):
        self.productDetails=[0,0,0,0]
        self.productDetails[0]=self.driver.find_element_by_xpath("//h1[@class='roboto-regular screen768 ng-binding']").text
        price= self.driver.find_element_by_xpath("//h2[@class='roboto-thin screen768 ng-binding']").text
        self.productDetails[2] =priceToFloat(price)
        self.productDetails[3] = self.driver.find_element_by_xpath("//span[contains(@class,'colorSelected')]").get_attribute('title')
        return self.productDetails
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
        details[2]=round(details[2]*quantity,2)
        self.addToCart()
        return details
    #Prints product details
    #Will not print the full details if the add new product function has'nt been executed.
    def printProductDetails(self):
        for j in range(4):
            if (j == 0):
                print(f'Name {self.productDetails[j]}', end="   ")
            if (j == 1):
                print(f'Quantity {self.productDetails[j]}', end="   ")
            if (j == 2):
                print(f'Price {self.productDetails[j]}', end="   ")
            if (j == 3):
                print(f'Color {self.productDetails[j]}')
    #Wait for the page to load.
    def implicityWaitProductPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Description")))
    #Reducing the quantity
    def reduceQuantity(self,amount):
        self.implicityWaitProductPage()
        for i in range(amount):
            try:
                self.driver.find_element_by_xpath("//div[@class='minus']").click()
            except:
                break
        self.addToCart()
#Shopping cart page class
class shoppingCart:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
    #Returns the the elements in the cart
    #List of names[0],List of quantity[1],List of price[2],List of color[3]
    def elements_in_cart(self):
        elements=[0,0,0,0]
        table="//table[@class='fixedTableEdgeCompatibility']//tr"
        elements[0]=self.driver.find_elements_by_xpath(f'{table}//label[@class="roboto-regular productName ng-binding"]')
        elements[1]=self.driver.find_elements_by_xpath(f'{table}//label[@class="ng-binding"]')
        elements[2]=self.driver.find_elements_by_xpath(f'{table}//p[@class="price roboto-regular ng-binding"]')
        elements[3] = self.driver.find_elements_by_xpath(f'{table}//span[@title]')
        return elements
    #Return the list of the products in the cart.
    # Returns list-it's length- the amount of the  products in cart
    # in each cell in the list the prodcut details order by:
    # Name[0], Quantity[1]=0-Cant Reach, Price[2], Color[3]
    def products_details(self):
        elements = self.elements_in_cart()
        self.product_list=[]
        for i in range (0,len(elements[0])):
            self.product_list.append([0,0,0,0])
        for i in range (0,len(elements[0])):
            self.product_list[i][0]=elements[0][i].text
            self.product_list[i][1] = elements[1][i].text
            price=elements[2][i].text
            self.product_list[i][2] =priceToFloat(price)
            self.product_list[i][3] = elements[3][i].get_attribute('title')
        return self.product_list
    #Return the check out price
    def checkOut(self):
        price=self.driver.find_element_by_xpath("//div[@id='shoppingCart']//span[@class='roboto-medium ng-binding']").text
        price=priceToFloat(price)
        return price
    #Click on the check out button
    def checkOutButtonClick(self):
        self.implicityWaitCartPage()
        self.driver.find_element_by_id("checkOutButton").click()
    #Waiting until the page is up
    def implicityWaitCartPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'SHOPPING CART')]"))
        )

    #Click on the edit button for the given location
    def editProduct(self,location):
        self.implicityWaitCartPage()
        editloc=self.driver.find_elements_by_xpath("//a[@class='edit ng-scope']")
        editloc[location].click()
#Order Payment pages
class orderPayment:
    #Constructor
    def __init__(self,driver):
        self.driver=driver
        self.userNameList=[]
    #1-Implicity wait- register page
    def waitRegisterPage(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID,"registerPage")))
    #2-Implicity wait- register button from shopping cart
    def waitRegisterButton(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "registration_btnundefined")))
    #3-Wait for the "Register" button to be clickable
    def waitRegisterButtonToBeClickAble(self):
        try:
            WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable((By.ID, "register_btnundefined")))
        except:
            return False
        return True
    #4-Implicity wait- Next button
    def waitNextButton(self):
        WebDriverWait(self.driver,20).until(
            EC.visibility_of_element_located((By.ID,"next_btn")))
    #5a(optional) Implicity wait after clicking on the next button-masterCredit
    def waitAfterNextButtonMasterCredit(self):
        WebDriverWait(self.driver,20).until(
            EC.visibility_of_element_located((By.ID,"paymentMethod")))
    #5b-Implicity wait-After clicking on the Next button
    def waitAfterNextButtonSafePay(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//sec-view[@a-hint='SafePay username']//div[@class='inputContainer ng-scope']")))
    #6-Implicity wait-after Payment
    def waitAfterPayment(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID,"orderPaymentSuccess")))
    #Click on the register button
    def registerButtonClick(self):
        self.waitRegisterButton()
        self.driver.find_element_by_id("registration_btnundefined").click()
    #Create new random user
    def User_name(self):
        self.st= 'kobi'
        num=random.randint(1,10000000)
        self.st=self.st+str(num)
        if(self.st in self.userNameList):
            return self.User_name()
        else:
            self.userNameList.append(self.st)
            return self.st
    #Create new account
    def Create_account(self):
        self.driver.find_element_by_xpath("//div//input[@name='usernameRegisterPage']").send_keys(self.User_name())
        self.driver.find_element_by_xpath('//div//input[@name="emailRegisterPage"]').send_keys('abcd@gmail.com')
        self.driver.find_element_by_xpath('//div//input[@name="passwordRegisterPage"]').send_keys('Ako123987')
        self.driver.find_element_by_xpath('//div//input[@name="confirm_passwordRegisterPage"]').send_keys('Ako123987')
        self.driver.find_element_by_name('i_agree').click()
        while (self.waitRegisterButtonToBeClickAble()==False):#Flaky button
            self.driver.find_element_by_name('i_agree').click()
        self.driver.find_element_by_id("register_btnundefined").click()
        enteredRegisterPage=False
        while(enteredRegisterPage==False):
            try:
                self.waitRegisterPage()#Flaky button
            except:
                self.driver.find_element_by_id("register_btnundefined").click()
            else:
                enteredRegisterPage = True
    #Create new payment method
    def PaymentSafePay(self):
        self.driver.find_element_by_id("next_btn").click()
        self.waitAfterNextButtonSafePay()
        self.driver.find_element_by_xpath(
            "//sec-view[@a-hint='SafePay username']//div[@class='inputContainer ng-scope']").click()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//sec-view[@a-hint='SafePay username']//label[@class='animated']")))
        self.driver.find_element_by_name("safepay_username").send_keys('Abcd12')
        self.driver.find_element_by_xpath("//sec-view[@a-hint='SafePay password']//div[@class='inputContainer ng-scope']").click()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//sec-view[@a-hint='SafePay password']//label[@class='animated']")))
        self.driver.find_element_by_name("safepay_password").send_keys('Barg1234')
        self.driver.find_element_by_id("pay_now_btn_SAFEPAY").click()
    # Create new payment method
    def PaymentMasterCredit(self):
        self.driver.find_element_by_id("next_btn").click()
        self.waitAfterNextButtonMasterCredit()
        self.driver.find_element_by_id("pay_now_btn_MasterCredit").click()
    #Return the order id
    def order_id(self):
        WebDriverWait(self.driver,5)
        return self.driver.find_element_by_id("orderNumberLabel").text
    #Creating new account in checkout section process
    def createAccountProcess(self):
        self.registerButtonClick()
        self.waitRegisterPage()
        self.Create_account()
        self.waitNextButton()
    #Creating new account and payment method
    def paymentProcessSafePay(self):
        self.createAccountProcess()
        self.PaymentSafePay()
        self.waitAfterPayment()
        return self.order_id()
    #The full process of the masterCredit payment
    def paymentProcessMasterCredit(self):
        self.waitNextButton()
        self.PaymentMasterCredit()
        self.waitAfterPayment()
        return self.order_id()





