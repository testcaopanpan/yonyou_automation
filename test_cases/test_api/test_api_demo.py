# _*_ coding:utf-8 _*_
import pytest
import requests
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import allure
from common.logger import logger

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
@allure.epic("API自动化")
@allure.feature("基础接口")
@allure.story("demo接口验证")
def test_api_demo():
    # 将cookie转换为字典
 #   cookie_dict = {cookie['name']: cookie['value'] for cookie in login_cookie}

    # 发送请求
    url = "https://jsonplaceholder.typicode.com/todos/1"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)

    # 记录日志
    logger.info(f"请求URL: {url}")
    logger.info(f"请求头: {headers}")
    logger.info(f"响应状态码: {response.status_code}")
    logger.info(f"响应内容: {response.text}")

    # 断言
    assert response.status_code == 200
    assert response.json()["id"] == 1    # 根据返回的 JSON 断言
@allure.epic("API自动化")
@allure.feature("基础接口")
@allure.story("生产订单发起打印请求验证")
def test_cache_print_api(login):
    cookie = get_cookie(login)
    url = "https://c2.yonyoucloud.com/mdf-node/cachePrint"
    header =  {
            "accept": "*/*",
            "accept-language": "zh,zh-CN;q=0.9",
            "content-type": "application/json;charset=UTF-8",
            "domain-key": "productionorder",
            "origin": "https://c2.yonyoucloud.com",
            "priority": "u=1, i",
            "referer": "https://c2.yonyoucloud.com/?fromYonyou=true",
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "x-xsrf-token": "MDF_QBGMYFCGNT7I3CM5WTW9PXUV6!150223",
            "Cookie":cookie
        }
    payload = {
        "param": "{\"classifyCode\":\"PO.po_production_order\",\"billno\":\"po_production_order\",\"printcountswitch\":true,\"printrefreshinterval\":1000,\"context_path\":\"/mdf-node/uniform\",\"ids\":[\"2027403629626916865\",\"2027403028339359753\",\"2027394498553708552\"],\"printAction\":\"preview\",\"sysParams\":{},\"domainParams\":{\"billno\":\"po_production_order\",\"printcountswitch\":true,\"printrefreshinterval\":1000,\"context_path\":\"/mdf-node/uniform\",\"ids\":[\"2027403629626916865\",\"2027403028339359753\",\"2027394498553708552\"],\"printAction\":\"preview\",\"datas\":[{\"id\":\"2027403629626916865\",\"orgId\":\"2236516150172672\",\"printTranstypeCode\":\"2229050875760927\",\"businessType\":\"yonbip-mm-mfpo\",\"businessId\":\"2027403629626916865\"},{\"id\":\"2027403028339359753\",\"orgId\":\"2236516150172672\",\"printTranstypeCode\":\"2229050875760927\",\"businessType\":\"yonbip-mm-mfpo\",\"businessId\":\"2027403028339359753\"},{\"id\":\"2027394498553708552\",\"orgId\":\"2236516150172672\",\"printTranstypeCode\":\"2229050875760927\",\"businessType\":\"yonbip-mm-mfpo\",\"businessId\":\"2027394498553708552\"}]},\"serviceCode\":\"po_production_order_list\"}",
        "billno": "po_production_order"
    }
    with allure.step("生产订单指定单据进行打印预览请求"):
        resp = requests.post(url=url,headers=header,json=payload)
        logger.info("请求的响应状态码是"+str(resp.status_code))
        logger.info("请求响应结果是:"+resp.json()["key"])
        key = resp.json()["key"]
        print(key)
        assert resp.json()["status"] == 1
        assert key is not None
    return key

@allure.epic("API自动化")
@allure.feature("基础接口")
@allure.story("获取生产订单可用模板列表")
def test_get_template_list(login):
    cookie = get_cookie(login)
    url = "https://c2.yonyoucloud.com/iuap-apcom-print/u8cprint/web/template/getTemplatesPrintForQuery"
    header = {
        "accept": "*/*",
        "accept-language": "zh,zh-CN;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "domain-key": "productionorder",
        "origin": "https://c2.yonyoucloud.com",
        "priority": "u=1, i",
        "referer": "https://c2.yonyoucloud.com/?fromYonyou=true",
        "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "x-xsrf-token": "MDF_QBGMYFCGNT7I3CM5WTW9PXUV6!150223",
        "Cookie": cookie
    }
    payload = {
        "meta":5,"parentcode":"PO","busiObj":"productionorder.po_production_order","classifyCodeName":"生产订单","billNum":"[\"po_production_order\",\"po_production_order_list\",\"po_production_order_ustock\",\"po_production_order_std\",\"po_production_order_inner_pull\",\"po_production_order_materialprint\",\"po_order_dimensional_materialprint\",\"po_daily_production_schedule_list\",\"po_cost_collect_order_list\",\"po_cost_collect_order\",\"dcrp_production_order_list\",\"po_order_material_sum_list\"]",
        "queryDomain":"productionorder"
    }
    with allure.step("查询生产订单可用模板"):
        resp = requests.post(url=url, headers=header, json=payload)
        logger.info("请求的响应状态码是" + str(resp.status_code))
        assert resp.status_code == 200
        assert isinstance(resp.json(),list),"响应体不是列表类型"
        ids = [item["code"] for item in resp.json() if "code" in item]
        assert len(ids) > 0
        logger.info("获取的可用模板列表为"+str(ids))
    return ids