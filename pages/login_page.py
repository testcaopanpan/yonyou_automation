# _*_ coding:utf-8 _*_
from selenium.webdriver.common.by import By
from common.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    # 元素定位
    username_input = (By.ID, 'username')
    password_input = (By.ID, 'password')
    login_button = (By.ID, 'loginBtn')

    def login(self, username, password):
        #启动浏览器并进入登录页面
        driver = webdriver.Chrome()
        driver.get("https://c2.yonyoucloud.com")
        driver.maximize_window()
        #等待并切换iframe
        WebDriverWait(driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, 'yonbip_login_id'))
        )
        print("成功切换到登录frame")
        # 3. 等待用户名输入框出现
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        self.send_keys(self.username_input, "yyptcloud@test1988.com")
        self.send_keys(self.password_input, "yypt@cloud2403")
        self.click(driver.find_element(by=By.NAME, value='submit_btn'))

        cookie = driver.get_cookie()
        return cookie