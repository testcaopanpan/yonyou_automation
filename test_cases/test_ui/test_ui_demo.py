from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def test_yongyou_login(login):
    driver = login

        # 验证登录结果
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="menu_img"]'))
        )
        print("登录成功！")
        element = driver.find_element(By.XPATH, '//*[@fieldid="menu_img"]')
        assert element is not None
    except TimeoutException:
        print("登录失败，用户名或密码错误！")