import os
import order.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        super(Order, self).__init__()


        self.driver.implicitly_wait(15)
        self.driver.maximize_window()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        
        if self.teardown == True:
            
            self.driver.quit()

    def land_first_page(self):

        listt = []

        self.driver.get(const.BASE_URL)

        self.driver.find_element(By.CSS_SELECTOR, "input[class='search-keyword']").send_keys("ber")

        time.sleep(4)

        buttons = self.driver.find_elements(By.XPATH, "//div[@class='product-action']/button")

        count = len(buttons)

        assert count == 3

        for i in buttons:

            i.click()

            listt.append(i.find_element(By.XPATH, "parent::div/parent::div/h4").text)

        print(listt)

        
        self.driver.find_element(By.CSS_SELECTOR, "img[alt='Cart']").click()

        self.driver.find_element(By.XPATH, "//button[text()='PROCEED TO CHECKOUT']").click()




