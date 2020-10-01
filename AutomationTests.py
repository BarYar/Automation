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
import logging
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
        self.mpage.enterCategoryPage(self.lCategory[self.categorynum])
        cpage = categoryPage(self.driver)
        ListOfLoc=[]
        cpage.openRandomProduct(ListOfLoc)
        ppage = productPage(self.driver)
        ppage.addNewProduct(3)
        cpage.backAndWait()
        cpage.openRandomProduct(ListOfLoc)
        ppage.addNewProduct(2)
        mpage=MainPage(self.driver)
        self.assertTrue(int(mpage.cartAmount())==5)
    #q2-Ordering 3 prodcuts,check if their details in the car are right.
    def test2(self):
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
    #q3- Ordering 2 products then remove 1 of them from the cart and check if it's removed from the cart.
    def test3(self):
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
    #q4-Ordering 2 products and then clicking on the shopping cart, check if we entered to the shopping cart
    def test4(self):
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
    #q5-Ordering 3 products, check if the total price of the products matches the checkout price.
    def test5(self):
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
            cpage.backAndWait()
        shoppingc = shoppingCart(self.driver)
        self.mpage.cartClick()
        shoppingc.implicityWaitCartPage()
        checkoutprice=shoppingc.checkOut()
        sum=round(sum,2)
        checkoutprice=round(checkoutprice,2)
        self.assertEqual(checkoutprice,sum)
    #q6-Ordering 2 products, then change their quantity and check if it has been updated in the cart.
    def test6(self):
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
        productsDetails[0][1]=2
        productsDetails[1][1] = 2
        self.assertTrue(self.mpage.cartCompare(productsDetails))
    #q7-Order a tablet, then return to tablets category and to main page
    def test7(self):
        self.mpage.enterCategoryPage('tablets')
        Ppage=productPage(self.driver)
        cpage= categoryPage(self.driver)
        cpage.openRandomProduct([])
        Ppage.addNewProduct(1)
        cpage.backAndWait()
        self.assertTrue(cpage.categoryTitleEqual('TABLETS'))
        self.mpage.returnToMainPage()
    #q8-Make an order, create new acoount, pay with SafePay and check that the order id is in my orders section
    def test8(self):
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
        orderIdAfterPayment=orderp.paymentProcessSafePay()
        self.mpage.returnToMainPage()
        orderidOrders = User(self.driver).getLastOrderId()
        self.assertEqual(orderidOrders, orderIdAfterPayment)

    #q9-Make an order, create new acoount, pay with credit card and check that the order id is in my orders section
    def test9(self):
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
        orderIdAfterPayment=orderp.paymentProcessMasterCredit()
        self.mpage.returnToMainPage()
        orderidOrders=User(self.driver).getLastOrderId()
        self.assertEqual(orderidOrders,orderIdAfterPayment)
    #q10-Log in and Log out process
    def test10(self):
        log=User(self.driver)
        log.LogIn('By1zx','Cb12')
        log.LogOut()

if __name__=="__main__":
    unittest.main()
