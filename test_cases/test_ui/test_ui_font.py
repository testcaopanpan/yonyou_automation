# _*_ coding:utf-8 _*_
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_font_upload(login):
    driver = login
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="menu_img"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="menu_img"]').click()
    # 等待搜索标识的出现并点击
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="nav-domain"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="nav-domain"]').click()
    # 等待搜索框的出现并搜索打印模板后点击
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="search-input"]')))
    driver.find_element(By.XPATH, '//*[@class="search-input"]').send_keys("字体管理")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "searchTitle1")]/../ul/li[1]')))
    driver.find_element(By.XPATH, '//*[contains(@class, "searchTitle1")]/../ul/li[1]').click()

    #等待字体编码框出现并进行检查点验证
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="fontCode"]')))
    element = driver.find_element(By.XPATH,'//*[@id="fontCode"]')
    #元素存在性验证
    assert element is not None

