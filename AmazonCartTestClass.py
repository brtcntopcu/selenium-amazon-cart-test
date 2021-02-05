import logging
import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

logging.basicConfig(filename="results.log", level=logging.INFO)

class AmazonCartTest():

    def __init__(self):
        self.browser = webdriver.Chrome()

    def priceParse(self, x):
        price = x.split(" ")[0]
        price = price.replace(",", ".")
        return float(price)
    
    def login(self, mail, password):
        try:
            self.browser.get('https://www.amazon.com.tr')
            self.browser.maximize_window()
            self.browser.find_element_by_xpath('//*[@id="nav-link-accountList"]').click()
            self.browser.find_element_by_xpath('//*[@id="ap_email"]').send_keys(mail)
            self.browser.find_element_by_xpath('//*[@id="continue"]').click()
            self.browser.find_element_by_xpath('//*[@id="ap_password"]').send_keys(password)
            self.browser.find_element_by_xpath('//*[@id="signInSubmit"]').click()
            logging.info('Login Successful')
        except (e):
            logging.error('Login Failed')

    def closeBrowser(self):
        self.browser.close()
    
    def addCartAnyProduct(self, product_url):
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-logo-sprites"]')))
            self.browser.get(product_url)
            self.browser.find_element_by_xpath('//*[@id="add-to-cart-button"]').click()
            logging.info('Product Add Succesful')
        except (e):
            logging.error('Product Add Failed')
        
    def goCart(self):
        try:
            self.browser.find_element_by_xpath('//*[@id="nav-cart"]').click()
            logging.info('Cart Opened')
        except (e):
            logging.error('Cart not Opened')

    def cartCheck(self):
        return int(self.browser.find_element_by_xpath('//*[@id="nav-cart-count"]').text)
        
    def cartTotalCheck(self):
        unitPrice = self.browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[7]/div/div[2]/div[3]/div/form/div[2]/div[3]/div[4]/div/div[2]/p/span').text.split(" ")[0]
        select = Select(self.browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[7]/div/div[2]/div[3]/div/form/div[2]/div[3]/div[4]/div/div[1]/div/div/div[2]/div[1]/span[1]/span/span[1]/span/select'))
        quantity = 7 #This quantity should be between 1 and 10 because select menu range is 1 and 10
        select.select_by_visible_text(str(quantity))
        time.sleep(2)
        total = self.browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[7]/div/div[1]/div[2]/div/form/div/div/div[1]/span[2]/span').text.split(" ")[0]
        if round(self.priceParse(unitPrice)*quantity, 2) == self.priceParse(total):
            logging.info("Test Pass")
        elif round(self.priceParse(unitPrice)*quantity, 2) != self.priceParse(total):
            logging.error("Test Fail")
        
    def clearCart(self):
        buttonList = self.browser.find_elements_by_css_selector('input[type="submit"][name^="submit.delete"]')
        my_element_id = 'input[type="submit"][name^="submit.delete"]'
        ignored_exceptions=[StaleElementReferenceException]

        while len(buttonList) > 0: # I used this. Because I'm getting a StaleElementReferenceException error. I've tried webdriverwait, ec etc. solutions without while loop but couldnt fix
            for b in buttonList:
                try:
                    my_element = WebDriverWait(self.browser, 10,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CSS_SELECTOR, my_element_id)))
                    my_element.click()
                    buttonList.remove(b)
                except StaleElementReferenceException as e:
                    continue
        logging.info('All item removed from cart before start test')

