# _*_ coding:utf-8 _*_
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_print_template_search(login):
    '''
    用例名称：验证打印模板节点进入正常
    该用例需要与test_tenant_id_check串行，否则后续需要优化到该租户下执行
    '''
    driver = login
    driver.refresh()
    #等待左上角的全局标识并点击
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="menu_img"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="menu_img"]').click()
    #等待搜索标识的出现并点击
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="nav-domain"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="nav-domain"]').click()
    # 等待搜索框的出现并搜索打印模板后点击
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="search-input"]')))
    driver.find_element(By.XPATH, '//*[@class="search-input"]').send_keys("打印模板")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "searchTitle1")]/../ul/li[1]')))
    driver.find_element(By.XPATH, '//*[contains(@class, "searchTitle1")]/../ul/li[1]').click()

    #等待并检查进入打印模板节点成功
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid = "iprint-distribution-relations_btn"]')))
    element = driver.find_element(By.XPATH, '//*[@fieldid = "iprint-distribution-relations_btn"]')
    #元素文本验证
    assert element.text == "分配关系查询"

def test_search_lingyujieidan(login):
    '''
    用例名称：左侧树搜索并点击进入生产订单节点验证
    该用例建议与test_print_template_search串行
    '''
    driver = login
    #等待左侧树搜索框并录入生产订单节点名称
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@title="搜索模板分类"]')))
    driver.find_element(By.XPATH,'//*[@title="搜索模板分类"]').send_keys("生产订单")

    #等待菜单节点【生产订单】出现并点击进入
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_classifytree_tree_title_productionorder.po_production_order"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_classifytree_tree_title_productionorder.po_production_order"]').click()

    #等待新增按钮标识并验证
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_add-iconfont"]')))
    #新增模板按钮标识存在验证
    element = driver.find_element(By.XPATH,'//*[@fieldid="iprint_add-iconfont"]')
    #元素存在性验证
    assert element is not None

def test_template_status(login):
    driver = login
    #等待并复制系统模板并验证目标模板存在

    #模板启停验证
    #模板默认标签验证
    #模板删除验证