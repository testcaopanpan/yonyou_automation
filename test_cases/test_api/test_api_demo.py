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


@allure.epic("API自动化")
@allure.feature("基础接口")
@allure.story("demo接口验证")
@pytest.mark.api
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
