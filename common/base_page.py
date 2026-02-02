# _*_ coding:utf-8 _*_
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from common.logger import logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.info(f"找到元素: {locator}")
            return element
        except TimeoutException:
            logger.error(f"未找到元素: {locator}")
            raise

    def click(self, locator):
        self.find_element(locator).click()
        logger.info(f"点击元素: {locator}")

    def send_keys(self, locator, text):
        self.find_element(locator).send_keys(text)
        logger.info(f"输入文本: {text} 到元素: {locator}")

    def get_title(self):
        return self.driver.title