# _*_ coding:utf-8 _*_
import os.path
import os
import pytest


cookie_file =os.path.join(os.path.dirname(__file__),"..","..","Cookie","api_cookie.txt")
@pytest.fixture(scope="module")
def common_headers():
    '''这个方法用于集成通用header内容'''
    with open(cookie_file,'r',encoding='utf-8') as f:
        get_cookie = f.read().strip()
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
        "Cookie": get_cookie
    }
    return header