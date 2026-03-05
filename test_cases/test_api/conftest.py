# _*_ coding:utf-8 _*_
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import allure
from common.logger import logger

@pytest.fixture(scope="module")
def get_cookie(login):
    '''
    该方法用于为后续的接口自动化用例提供cookie
    '''
    driver = login
    driver.refresh()
    # 等待左上角的全局标识并点击
    with allure.step("等待左上角的全局标识并点击"):
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="menu_img"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="menu_img"]').click()
    # 等待搜索标识的出现并点击
    with allure.step("等待搜索标识的出现并点击并进入生产订单节点"):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="nav-domain"]')))
        driver.find_element(By.XPATH, '//*[@fieldid="nav-domain"]').click()
        # 等待搜索框的出现并搜索生产订单后点击
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="search-input"]')))
        driver.find_element(By.XPATH, '//*[@class="search-input"]').send_keys("生产订单")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "searchTitle1")]/../ul/li[1]')))
        driver.find_element(By.XPATH, '//*[contains(@class, "searchTitle1")]/../ul/li[1]').click()
        #进入生产订单节点成功
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@fieldid="po_production_order_list|btnPrintDrop_btn"]')))
        assert driver.find_element(By.XPATH,'//*[@fieldid="po_production_order_list|btnPrintDrop_btn"]') is not None
    with allure.step("通过生产订单节点拿取当前cookie"):
        selenium_cookie = driver.get_cookies()
        requests_cookie = {cookie["name"]:cookie["value"] for cookie in selenium_cookie}
        logger.info("将字典型cookie结构转化成字符串型")
        cookie_str = ";".join([f'{key}={value}' for key,value in requests_cookie.items()])
    return cookie_str