import os
import order.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import time



class Order:

    def __init__(self, driver_path = r"C:/SeleniumDrivers", teardown = False):

        self.driver_path = driver_path
        self.teardown = teardown

        os.environ['PATH'] += self.driver_path

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        
        if self.teardown == True:
            
            self.driver.quit()

    def land_first_page(self):

        self.listt = []

        self.driver.get(const.BASE_URL)

        self.driver.find_element(By.CSS_SELECTOR, "input[class='search-keyword']").send_keys("ber")

        time.sleep(4)

        buttons = self.driver.find_elements(By.XPATH, "//div[@class='product-action']/button")

        count = len(buttons)

        assert count == 3

        for i in buttons:

            i.click()

            self.listt.append(i.find_element(By.XPATH, "parent::div/parent::div/h4").text)

        for i in self.listt:

            assert 'ber' in i
        
        self.driver.find_element(By.CSS_SELECTOR, "img[alt='Cart']").click()

        self.driver.find_element(By.XPATH, "//button[text()='PROCEED TO CHECKOUT']").click()


    def cart(self):

        listt2 = []

        products = self.driver.find_elements(By.CSS_SELECTOR, "p.product-name")

        for i in products:
            if i.text == "":
                continue
            else:
                listt2.append(i.text)

        assert self.listt == listt2, "Last Page's Products are not appeared in the cart properly"

        total_amount = int(self.driver.find_element(By.CSS_SELECTOR, ".totAmt").text)

        summ = 0

        store = 0

        per_product_total = self.driver.find_elements(By.XPATH, "//tr/td[5]/p")

        for i in per_product_total:

            summ = store+int(i.text)

            store = summ

        assert total_amount == summ, "Total Amount is not properly showing"
        

        self.driver.find_element(By.CSS_SELECTOR, "input[class='promoCode']").send_keys("rahulshettyacademy")

        time.sleep(5)

        self.driver.find_element(By.CSS_SELECTOR, ".promoBtn").click()

        time.sleep(8)

        discounted_price = total_amount-(total_amount*0.1)

        actual_discounted_price = float(self.driver.find_element(By.CSS_SELECTOR, ".discountAmt").text)

        assert float(total_amount)>actual_discounted_price

        assert discounted_price==actual_discounted_price

        self.driver.find_element(By.XPATH, "//button[text()='Place Order']").click()

    def placeorder(self):

        dropdown = Select(self.driver.find_element(By.CSS_SELECTOR, 'select[style="width: 200px;"]'))

        dropdown.select_by_visible_text("Bangladesh")

        self.driver.find_element(By.XPATH, "//button[text()='Proceed']").click()

        try:

            warning = self.driver.find_element(By.CSS_SELECTOR, "b")
            
            assert warning is not None
        
        except NoSuchElementException:
        
            assert False, "No Warning for not accepting terms and conditions"
        

        self.driver.find_element(By.XPATH, "//button[text()='Proceed']").click()

        self.driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]').click()

        self.driver.find_element(By.XPATH, "//button[text()='Proceed']").click()
