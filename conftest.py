# _*_ coding:utf-8 _*_
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def handle_notification_popup(driver):
    """处理浏览器通知权限弹窗"""
    try:
        # 等待弹窗出现（最多10秒）
        allow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='接受']"))
        )
        allow_button.click()
        print("已确认隐私权限")
    except TimeoutException:
        print("未检测到隐私权限弹窗，跳过处理")
    except Exception as e:
        print(f"处理通知权限弹窗失败: {e}")

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def login(driver):
    driver.get("https://c2.yonyoucloud.com")
    driver.maximize_window()
    # 处理隐私弹窗
    handle_notification_popup(driver)
    # 切换到登录frame
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'yonbip_login_id'))
    )
    # 输入用户名和密码
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(by=By.ID, value='username').send_keys('yyptcloud@test1988.com')
    driver.find_element(by=By.ID, value='password').send_keys('yypt@cloud2403')
    # 点击登录按钮
    driver.find_element(by=By.NAME, value='submit_btn').click()
    # 切换回主文档
    driver.switch_to.default_content()
    # 验证登录结果
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@fieldid="menu_img"]'))
    )
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="userAvatorNew_img"]')))
    # 点击右上角的用户标识
    driver.find_element(By.XPATH, '//*[@fieldid="userAvatorNew_img"]').click()
    # 等待退出按钮标识出现
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@fieldid="settings-item-logout_btn"]')))

    # 检查并切换至目标租户后检查当前租户名称是否为测试租户
    element = driver.find_element(By.XPATH, '//*[@class="home_title"]/span[1]')
    if element.text != "0422专业全产品":
        element.click()
        driver.find_element(By.ID, 'searchId').send_keys("0422专业全产品")
        # 等待搜索租户出现并点击
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[text()="0422专业全产品"]')))
        driver.find_element(By.XPATH, '//*[text()="0422专业全产品"]').click()
        # 等待二次确认弹窗出现并点击
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="tenanToggle_ok_btn"]')))
        driver.find_element(By.XPATH, '//*[@fieldid="tenanToggle_ok_btn"]').click()

        # 再次等待用户标识的出现并点击
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="userAvatorNew_img"]')))
        driver.find_element(By.XPATH, '//*[@fieldid="userAvatorNew_img"]').click()
    else:
        driver.refresh()
    return driver