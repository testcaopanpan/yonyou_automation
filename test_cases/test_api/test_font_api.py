# _*_ coding:utf-8 _*_

import allure
import json
import requests
from common.logger import logger

@allure.story("删除指定用例")
def font_delete(common_headers,id):
    '''
    该接口是删除指定字体的接口
    '''
    url = "https://c2.yonyoucloud.com/iuap-apcom-print/u8cprint/font/v2/deleteFont"
    payload = [f'{id}']
    allure.step("执行删除指定字体")
    logger.info("执行删除指定字体")
    font_delete_res = requests.post(url=url, data=json.dumps(payload), headers=common_headers)
    allure.step("执行删除用例完成,执行检查点命令")
    logger.info("指定字体删除成功")
    assert font_delete_res.json()["message"] == "OK"

@allure.story("上传指定字体")
def upload_font(common_headers):
    '''
    该接口用于指定字体的上传
    '''
    url = "https://c2.yonyoucloud.com/iuap-apcom-print/u8cprint/font/v2/uploadFont"
    file_path = "E:/Users/caopanpan/Downloads/HFIntimate-2.ttf"
    with open(file_path, 'rb') as f:
        files = {
            'file': (file_path.split('/')[-1], f, 'application/octet-stream')
        }

        logger.info(f"调用上传接口: {url}")
        logger.info(f"上传文件: {file_path}")
        # 发送上传请求
        response = requests.post(url=url,headers=common_headers,files=files)
        assert response.status_code == 200

@allure.story("进行字体查询")
def chaxun_font(common_headers):
    url = "https://c2.yonyoucloud.com/iuap-apcom-print/u8cprint/font/v2/pageFont?code=&name=&current=1&size=1000"
    with allure.step("前置请求：获取当前租户的全部自定义上传字体"):
        res = requests.get(url,headers=common_headers)
        logger.info("请求状态码是："+str(res.status_code))
        logger.info("请求结果的响应体如下：\n"+res.text)
        assert res.status_code == 200
        return res.json()['data']


@allure.epic("API自动化")
@allure.feature("字体接口")
@allure.story("进行字体上传、查询、删除验证")
def test_font_check(common_headers):
    record_list = chaxun_font(common_headers).get("recordList", [])
    target_font_name = "HFIntimate"
    for font in record_list:
        if font.get('name') == target_font_name:
            id = font.get('id')
            allure.step("删除本地的目标原字体")
            font_delete(common_headers,id)
            allure.step("目标字体删除完成")
        else:
            logger.info("当前字体不是目标字体。")
    allure.step("进行指定字体的上传")
    upload_font(common_headers)
    allure.step("再次进行字体列表查询")
    record_list1 = chaxun_font(common_headers).get("recordList", [])
    for font in record_list1:
        if font.get('name') == target_font_name:
            assert target_font_name is not None
            id = font.get('id')
            allure.step("删除本地的目标原字体")
            font_delete(common_headers,id)
            allure.step("目标字体删除完成")







