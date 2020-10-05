from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from unittest import TestCase
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from AutomationClasses import *
from Loger import logTest,logFails
class TestAOS(TestCase):
    #Set up method
    def setUp(self):
        path = r"C:\Users\97252\Desktop\Selenium\chromedriver.exe"
        self.driver = webdriver.Chrome(path)
        self.driver.get("https://www.advantageonlineshopping.com/#/")
        self.lCategory=['speakers','tablets','laptops','mice','headphones']
        self.driver.maximize_window()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
        self.mpage = MainPage(self.driver)
        self.categorynum = random.randint(0, 4)
    #Tear down method
    def tearDown(self):
        self.driver.find_element_by_class_name("logo").click()
        self.driver.quit()
    #q1-Add 2 products-check if it's equal to the amount of products in the top right of the screen
    def test1(self):
        try:
            self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
            cpage = categoryPage(self.driver)
            ListOfLoc=[]
            ppage = productPage(self.driver)
            for i in range(2):
                cpage.openRandomProduct(ListOfLoc)
                ppage.addNewProduct(3 - i)
                cpage.backAndWait()
            self.assertTrue(int(self.mpage.cartAmount())==5)
            logTest("INFO", 1)
        except:
            logTest("ERROR", 1)
            logFails(1)
            self.fail()
    #q2-Ordering 3 prodcuts,check if their details in the cart are right.
    def test2(self):
        try:
            self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
            cpage = categoryPage(self.driver)
            ListOfLoc =[]
            productsDetails=[]
            ppage = productPage(self.driver)
            for i in range(3):
                cpage.openRandomProduct(ListOfLoc)
                productsDetails.append(ppage.addNewProduct(3-i))
                cpage.backAndWait()
            self.assertTrue(self.mpage.cartCompare(productsDetails))
            logTest("INFO", 2)
        except:
            logTest("ERROR", 2)
            logFails(2)
            self.fail()
    #q3- Ordering 2 products then remove 1 of them from the cart and check if it's removed from the cart.
    def test3(self):
        try:
            self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
            cpage = categoryPage(self.driver)
            ListOfLoc = []
            ppage = productPage(self.driver)
            for i in range(2):
                cpage.openRandomProduct(ListOfLoc)
                ppage.addNewProduct(3 - i)
                cpage.backAndWait()
            productr=self.mpage.cartRemove()
            self.assertFalse(self.mpage.isInCart(productr))
            logTest("INFO", 3)
        except:
            logTest("ERROR", 3)
            logFails(3)
            self.fail()
    #q4-Ordering 2 products and then clicking on the shopping cart, check if we entered to the shopping cart
    def test4(self):
        try:
            self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
            cpage = categoryPage(self.driver)
            ListOfLoc = []
            ppage = productPage(self.driver)
            for i in range(2):
                cpage.openRandomProduct(ListOfLoc)
                ppage.addNewProduct(3 - i)
                cpage.backAndWait()
            self.mpage.cartClick()
            cartp=shoppingCart(self.driver)
            cartp.implicityWaitCartPage()
            logTest("INFO", 4)
        except:
            logTest("ERROR", 4)
            logFails(4)
            self.fail()
    #q5-Ordering 3 products, check if the total price of the products matches the checkout price.
    #In addition, you need to print each product details
    def test5(self):
        try:
            self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
            cpage = categoryPage(self.driver)
            ListOfLoc = []
            productsDetails = []
            sum=0
            ppage = productPage(self.driver)
            for i in range(3):
                cpage.openRandomProduct(ListOfLoc)
                productsDetails.append(ppage.addNewProduct(3 - i))
                sum=sum+productsDetails[i][2]
                if(i==0):
                    print("The products details are:")
                ppage.printProductDetails()
                cpage.backAndWait()
            shoppingc = shoppingCart(self.driver)
            self.mpage.cartClick()
            shoppingc.implicityWaitCartPage()
            checkoutprice=shoppingc.checkOut()
            sum=round(sum,2)
            checkoutprice=round(checkoutprice,2)
            self.assertEqual(checkoutprice,sum)
            logTest("INFO", 5)
        except:
            logTest("ERROR", 5)
            logFails(5)
            self.fail()
    #q6-Ordering 2 products, then change their quantity and check if it has been updated in the cart.
    def test6(self):
        try:
            self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
            cpage = categoryPage(self.driver)
            ListOfLoc = []
            ppage = productPage(self.driver)
            for i in range(2):
                cpage.openRandomProduct(ListOfLoc)
                ppage.addNewProduct(3)
                cpage.backAndWait()
            productsDetails=self.mpage.getProductDetails()
            self.mpage.cartClick()
            cartpage=shoppingCart(self.driver)
            cartpage.editProduct(1)
            ppage.reduceQuantity(1)
            self.mpage.cartClick()
            cartpage.editProduct(1)
            ppage.reduceQuantity(1)
            productsDetails[0][1] = 2
            productsDetails[1][1] = 2
            self.assertTrue(self.mpage.cartCompare(productsDetails))
            logTest("INFO", 6)
        except:
            logTest("ERROR", 6)
            logFails(6)
            self.fail()
    #q7-Order a tablet, then return to tablets category and to main page
    def test7(self):
        try:
            self.mpage.enterCategoryPage('tablets')
            Ppage=productPage(self.driver)
            cpage= categoryPage(self.driver)
            cpage.openRandomProduct([])
            Ppage.addNewProduct(1)
            cpage.backAndWait()
            self.assertTrue(cpage.categoryTitleEqual('TABLETS'))
            self.mpage.returnToMainPage()
            logTest("INFO", 7)
        except:
            logTest("ERROR", 7)
            logFails(7)
            self.fail()
    #q8-Make an order, create new acoount, pay with SafePay and check that the order id is in my orders section
    def test8(self):
        try:
            self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
            cpage = categoryPage(self.driver)
            ppage = productPage(self.driver)
            ListOfLoc = []
            for i in range(2):
                cpage.openRandomProduct(ListOfLoc)
                ppage.addNewProduct(3 - i)
                cpage.backAndWait()
            self.mpage.cartClick()
            shoppingc = shoppingCart(self.driver)
            shoppingc.checkOutButtonClick()
            orderp = orderPayment(self.driver)
            orderIdAfterPayment = orderp.paymentProcessSafePay()
            self.mpage.returnToMainPage()
            orderidOrders = User(self.driver).getLastOrderId()
            self.assertEqual(orderidOrders, orderIdAfterPayment)
            logTest("INFO", 8)
        except:
            logTest("ERROR", 8)
            logFails(8)
            self.fail()

    #q9-Make an order, enter existing acoount, pay with credit card and check that the order id is in my orders section
    def test9(self):
        try:
            self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
            cpage = categoryPage(self.driver)
            ppage = productPage(self.driver)
            ListOfLoc = []
            for i in range(2):
                cpage.openRandomProduct(ListOfLoc)
                ppage.addNewProduct(3 - i)
                cpage.backAndWait()
            self.mpage.cartClick()
            shoppingc = shoppingCart(self.driver)
            shoppingc.checkOutButtonClick()
            log = User(self.driver)
            log.LogIn('By123','Cer1')
            orderp = orderPayment(self.driver)
            orderIdAfterPayment = orderp.paymentProcessMasterCredit()
            self.mpage.returnToMainPage()
            orderidOrders=User(self.driver).getLastOrderId()
            self.assertEqual(orderidOrders,orderIdAfterPayment)
            logTest("INFO", 9)
        except:
            logTest("ERROR", 9)
            logFails(9)
            self.fail()
    #q10-Log in and Log out process
    def test10(self):
        try:
            log=User(self.driver)
            log.LogIn('By1zx', 'Cb12')
            log.LogOut()
            logTest("INFO",10)
        except:
            logTest("ERROR", 10)
            logFails(10)
            self.fail()

if __name__=="__main__":
    unittest.main()
