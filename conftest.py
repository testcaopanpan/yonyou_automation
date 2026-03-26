# _*_ coding:utf-8 _*_
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import allure
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from common.logger import logger


def save_debug_info(driver, step_name):
    """保存Jenkins执行时的页面截图、源码，用于排查"""
    # 创建调试目录
    debug_dir = "jenkins_debug"
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    # 保存截图
    screenshot_path = f"{debug_dir}/{step_name}_{time.strftime('%Y%m%d_%H%M%S')}.png"
    driver.save_screenshot(screenshot_path)
    print(f"已保存截图: {screenshot_path}")

    # 保存页面源码
    source_path = f"{debug_dir}/{step_name}_{time.strftime('%Y%m%d_%H%M%S')}.html"
    with open(source_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"已保存页面源码: {source_path}")
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
    options = Options()
    if os.getenv("HEADLESS","false").lower() in ("1","true","yes"):
        options.add_argument("--headless")
        options.add_argument("--disablue-gpu")
        options.add_argument("--no-sandbox")
    remote = os.getenv("SELENIUM_REMOTE_URL")
    if remote:
        driver = webdriver.Remote(command_executor=remote,options=options)
    else:
        driver = webdriver.Chrome(options=options)
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
    WebDriverWait(driver, 30).until(
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="menu_img"]'))
        )
        print("登录成功！")
        element = driver.find_element(By.XPATH, '//*[@fieldid="menu_img"]')
        assert element is not None
    else:
        driver.refresh()
    #return driver
    yield driver
    print("这是登录的teardown方法")
    allure.step("这是登录的teardown方法")
    logger.info("这是登录的teardown方法")
cookie_file = os.path.join(os.path.dirname(__file__),"Cookie","api_cookie.txt")
@pytest.fixture(scope="session")
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
        with open(cookie_file,'w',encoding='utf-8') as f:
            f.write(cookie_str)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    在每个测试阶段结束后，把结果对象挂在 item 上：
    - item.rep_setup
    - item.rep_call
    - item.rep_teardown
    方便后面的 fixture 判断用例是否失败。
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    '''
    所有使用了driver的ui用例都会自动套上这个fixture，
    用例执行完成后会自动检查是否失败，失败则调用save_screenshort
    '''
    yield
    driver = request.node.funcargs.get("driver", None)  # 自己去取，取不到就跳过
    if driver is None:
        return
    #只关注用例主体阶段的结果(rep_call)
    rep = getattr(request.node,"rep_call",None)
    #rep可能为None；确保有结果且用例失败的时候才截图
    if rep and rep.failed:
        # 以日期分目录：screenshots/20260225/xxx.png
        date_str = datetime.now().strftime("%Y%m%d")
        screenshot_dir = os.path.join("screenshorts",date_str)
        os.makedirs(screenshot_dir,exist_ok=True)
        # 用例名 + 时间戳 作为文件名，方便定位
        test_name = request.node.name
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        file_path = os.path.join(screenshot_dir,filename)
        try:
            driver.save_screenshot(file_path)
            print(f"用例执行失败，失败已截图至:{file_path}")
            # 新增：把截图挂到 Allure 报告里
            try:
                allure.attach.file(
                    file_path,
                    name=f"{test_name}_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as attach_err:
                print(f"将截图附加到 Allure 报告时出错：{attach_err}")
        except Exception as e:
            print(f"用例失败时截图失败：{e}")