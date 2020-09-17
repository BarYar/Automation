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
#Ordering 3 items and then checking if the items exist in the cart.
class TestAOS(TestCase):
    #setUp
    def setUp(self):
        path = r"C:\Driver\chromedriver.exe"
        self.driver = webdriver.Chrome(path)
        self.driver.get("https://www.advantageonlineshopping.com/#/")
        self.lCategory=['speakers','tablets','laptops','mice','headphones']
        self.driver.maximize_window()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element((By.CLASS_NAME, "loader"))
        )
    def tearDown(self):
        self.driver.find_element_by_class_name("logo").click()
        self.driver.quit()
    #q1-Add 2 products-check if it's equal to the amount of products in the top right.
    def test1(self):
        mpage=MainPage(self.driver)
        categorynum=random.randint(0,4)
        mpage.enterCategoryPage(self.lCategory[categorynum])
        cpage = categoryPage(self.driver)
        ListOfLoc=cpage.openRandomProduct()
        ppage = productPage(self.driver)
        ppage.addNewProduct(3)
        cpage.backAndWait()
        cpage.openRandomProduct(ListOfLoc)
        ppage.addNewProduct(2)
        mpage=MainPage(self.driver)
        assert mpage.cartAmount()==5



    #q10-Log in and Log out process
    def test10(self):
        log=Log(self.driver)
        log.LogInDetails('experis123','Experis123')
        log.LogIn()
        log.LogOut()


if __name__=="__main__":
    unittest.main()
# Ordering 2 items with different quantities and then checking if the items exist in the cart.
    # def test2(self):
    #     enteredProducts= []
    #     cartProducts= []
    #     try: #Entering the tablets category.
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.ID, "tabletsImg"))
    #         )
    #     except:
    #         self.fail()
    #     self.driver.find_element_by_id("tabletsImg").click()
    #     # Entering the first product page.
    #     try:
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.ID, "16"))
    #         )
    #     except:
    #         self.fail()
    #     self.driver.find_element_by_id("16").click()
    #     try:
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, "//h1[@class='roboto-regular ng-binding']"))
    #         )
    #     except:
    #         self.fail()
    #     #Entering the first product to the cart.
    #     enteredProducts=enteredProducts+[(self.driver.find_element_by_xpath("//h1[@class='roboto-regular screen768 ng-binding']").text),3,"BLACK",
    #                 self.driver.find_element_by_xpath('//h2[@class="roboto-thin screen768 ng-binding"]').text]
    #     actions=ActionChains(self.driver)
    #     actions.double_click(self.driver.find_element_by_xpath("//div[@class='plus']")).perform()
    #     self.driver.find_element_by_name("save_to_cart").click()
    #     # Entering the second product page.
    #     self.driver.find_element_by_xpath("//a[@class='ng-binding']").click()
    #     try:
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.ID, "17"))
    #         )
    #     except:
    #         self.fail()
    #     self.driver.find_element_by_id("17").click()
    #     try:
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, "//h1[@class='roboto-regular ng-binding']"))
    #         )
    #     except:
    #         self.fail()
    #     # Entering the second product to the cart.
    #     enteredProducts = enteredProducts + [
    #         (self.driver.find_element_by_xpath("//h1[@class='roboto-regular screen768 ng-binding']").text), 2, "BLACK",
    #         self.driver.find_element_by_xpath('//h2[@class="roboto-thin screen768 ng-binding"]').text]
    #     self.driver.find_element_by_xpath("//div[@class='plus']").click()
    #     self.driver.find_element_by_name("save_to_cart").click()
    #     # Entering the third product page.
    #     self.driver.find_element_by_xpath("//a[@class='ng-binding']").click()
    #     try:
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.ID, "18"))
    #         )
    #     except:
    #         self.fail()
    #     self.driver.find_element_by_id("18").click()
    #     try:
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, "//h1[@class='roboto-regular ng-binding']"))
    #         )
    #     except:
    #         self.fail()
    #     # Entering the third product to the cart.
    #     enteredProducts = enteredProducts + [
    #         (self.driver.find_element_by_xpath("//h1[@class='roboto-regular screen768 ng-binding']").text), 3, "BLACK",
    #         self.driver.find_element_by_xpath('//h2[@class="roboto-thin screen768 ng-binding"]').text]
    #     self.driver.find_element_by_xpath("//div[@class='plus']").click()
    #     self.driver.find_element_by_name("save_to_cart").click()
    #     try:
    #         element = WebDriverWait(self.driver, 30).until(
    #             EC.visibility_of_element_located((By.XPATH, f'// table / tbody / tr[2] / td[2] / a / label[1]'))
    #         )
    #     except:
    #         self.fail()
    #     #Adding the products in cart to the dictionary.
    #     #The method of working with rows in table, does'nt work with that table.
    #     for i in range(1, 4):
    #         cartProducts.append( self.driver.find_element_by_xpath(f'//table//tr[{i}]//h3[@class="ng-binding"]').text) #Add Name
    #         cartProducts.append(self.driver.find_element_by_xpath(f'//table//tr[{i}]//label[@class="ng-binding"]').text) #Add Quantity
    #         cartProducts.append(self.driver.find_element_by_xpath(f'//table//tr[{i}]//span[@class="ng-binding"]').text) #Add Color
    #         cartProducts.append(self.driver.find_element_by_xpath(f'//table//tr[{i}]//td[3]/p[@class="price roboto-regular ng-binding"]').text) #Add Price
    #     print(enteredProducts)
    #     print(cartProducts)
    #     # Check if the items exists in the cart.
    #     for i in enteredProducts:
    #         self.assertTrue(i in cartProducts)
    #         self.assertTrue(enteredProducts[i] == cartProducts[i])