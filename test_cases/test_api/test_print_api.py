# _*_ coding:utf-8 _*_
import time

import allure
import requests
from common.logger import logger

@allure.epic("API自动化")
@allure.feature("基础接口")
@allure.story("生产订单发起打印请求验证")
def test_cache_print_api(common_headers):
    url = "https://c2.yonyoucloud.com/mdf-node/cachePrint"
    payload = {
        "param": "{\"classifyCode\":\"PO.po_production_order\",\"billno\":\"po_production_order\",\"printcountswitch\":true,\"printrefreshinterval\":1000,\"context_path\":\"/mdf-node/uniform\",\"ids\":[\"2027403629626916865\",\"2027403028339359753\",\"2027394498553708552\"],\"printAction\":\"preview\",\"sysParams\":{},\"domainParams\":{\"billno\":\"po_production_order\",\"printcountswitch\":true,\"printrefreshinterval\":1000,\"context_path\":\"/mdf-node/uniform\",\"ids\":[\"2027403629626916865\",\"2027403028339359753\",\"2027394498553708552\"],\"printAction\":\"preview\",\"datas\":[{\"id\":\"2027403629626916865\",\"orgId\":\"2236516150172672\",\"printTranstypeCode\":\"2229050875760927\",\"businessType\":\"yonbip-mm-mfpo\",\"businessId\":\"2027403629626916865\"},{\"id\":\"2027403028339359753\",\"orgId\":\"2236516150172672\",\"printTranstypeCode\":\"2229050875760927\",\"businessType\":\"yonbip-mm-mfpo\",\"businessId\":\"2027403028339359753\"},{\"id\":\"2027394498553708552\",\"orgId\":\"2236516150172672\",\"printTranstypeCode\":\"2229050875760927\",\"businessType\":\"yonbip-mm-mfpo\",\"businessId\":\"2027394498553708552\"}]},\"serviceCode\":\"po_production_order_list\"}",
        "billno": "po_production_order"
    }
    with allure.step("生产订单指定单据进行打印预览请求"):
        resp = requests.post(url=url,headers=common_headers,json=payload)
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
def test_get_template_list(common_headers):
    url = "https://c2.yonyoucloud.com/iuap-apcom-print/u8cprint/web/template/getTemplatesPrintForQuery"
    payload = {
        "meta":5,"parentcode":"PO","busiObj":"productionorder.po_production_order","classifyCodeName":"生产订单","billNum":"[\"po_production_order\",\"po_production_order_list\",\"po_production_order_ustock\",\"po_production_order_std\",\"po_production_order_inner_pull\",\"po_production_order_materialprint\",\"po_order_dimensional_materialprint\",\"po_daily_production_schedule_list\",\"po_cost_collect_order_list\",\"po_cost_collect_order\",\"dcrp_production_order_list\",\"po_order_material_sum_list\"]",
        "queryDomain":"productionorder"
    }
    with allure.step("查询生产订单可用模板"):
        resp = requests.post(url=url, headers=common_headers, json=payload)
        logger.info("请求的响应状态码是" + str(resp.status_code))
        assert resp.status_code == 200
        assert isinstance(resp.json(),list),"响应体不是列表类型"
        ids = [item["code"] for item in resp.json() if "code" in item]
        assert len(ids) > 0
        logger.info("获取的可用模板列表为"+str(ids))
    return ids

@allure.epic("API自动化")
@allure.feature("基础接口")
@allure.story("实际单据进行最终打印预览使用的print接口")
def test_print(common_headers):
    url_print = "https://c2.yonyoucloud.com/iuap-apcom-print/iuap-print-pdf/pdf/print"
    para = test_cache_print_api(common_headers)
    ids = test_get_template_list(common_headers)
    logger.info(f"开始循环进行打印模板的预览接口请求，共{len(ids)}个模板")
    success_list = []
    failed_list = []
    with allure.step(f"开始循环进行打印模板的预览接口请求，共{len(ids)}个模板"):
        for index,code in enumerate(ids,1):
            try:
                payload ={
                "appSource": "PO",
                "domainDataBaseByCode": "MF",
                "tenantId": "w1a1kdwu",
                "printcode": f"{code}",
                "meta": "5",
                "sendType": "7",
                "lang": "zh_CN",
                "orgId": "2236516150172672",
                "sysLocale": "zh_CN",
                "params": f"{para}",
                "serviceCode": "po_production_order_list",
                "serverUrl": "https://c2.yonyoucloud.com/mdf-node/formdata//bill/getPrintData?domainKey=productionorder&serviceCode=po_production_order_list",
                "newArch": "true",
                "multilingualFlag": "true",
                "locale": "zh_CN",
                "previewUrl": "https://c2.yonyoucloud.com/iuap-apcom-print/u8cprint/design/getPreview",
                "split": "false",
                "isCache": "1",
                "keepAlive": "true",
                "classifyCodeForCount": "PO.po_production_order"
            }
                with allure.step(f"测试模板 {index}/{len(ids)}: {code}"):
                    resp = requests.post(url=url_print,headers=common_headers,json=payload)
                    time.sleep(2)
                    logger.info(f"{code}模板打印预览请求的响应状态码为"+str(resp.status_code))
                    if resp.status_code == 200:
                        if "PDF-" in resp.json()["data"]:
                            success_list.append(code)
                            logger.info(f"✓ 模板 {code} 打印预览成功")
                        else:
                            failed_list.append(code)
                            logger.info(f"× 模板 {code} 打印预览失败")
                    else:
                        failed_list.append(code)
                        logger.error(f"✗ 模板 {code} 失败：HTTP状态码异常 {resp.status_code}")
            except Exception as e:
                failed_list.append(code)
                logger.error(f"✗ 模板 {code} 异常: {str(e)}")

    allure.step("成功的打印模板清单如下"+success_list)
    allure.step("失败的打印模板清单如下"+failed_list)
    logger.info("成功的打印模板清单如下"+success_list)
    logger.info("失败的打印模板清单如下"+failed_list)

