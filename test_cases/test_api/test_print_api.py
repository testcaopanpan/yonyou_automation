# _*_ coding:utf-8 _*_
import csv
import os.path
import time
import zipfile
from requests.exceptions import HTTPError
import allure
import pytest
import requests
from common.logger import logger

@allure.epic("API自动化")
@allure.feature("基础接口")
@allure.story("生产订单发起打印请求验证")
@pytest.mark.api
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
@pytest.mark.api
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
@pytest.mark.api
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
                    time.sleep(0.5)
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

    allure.step("成功的打印模板清单如下"+str(success_list))
    allure.step("失败的打印模板清单如下"+str(failed_list))
    logger.info("成功的打印模板清单如下"+str(success_list))
    logger.info("失败的打印模板清单如下"+str(failed_list))


csv_file_path =f"D://python_workspace//yonyou_automation//data.csv"
def load_test_data(csv_file_path):
    """
        从CSV文件中加载测试数据
        CSV格式：
        file:E:\compare\compare_json\DYMB_119.zip
        originalPdf:E:\compare\compare_pdf\DYMB_119.zip
        expected_re:一致
        """
    test_data = []
    with open(csv_file_path,'r',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 解析每一行，假设CSV有列名：file, originalPdf, expected_re
            file_path = row['file']
            originalPdf_path = row['originalPdf']
            excepted_result = row['excepted_re']
            test_data.append((file_path,originalPdf_path,excepted_result))
    logger.info(f"从{csv_file_path}加载了{len(test_data)}条测试数据")
    return test_data
@allure.epic("API自动化")
@allure.feature("基础接口")
@allure.story("compare接口场景执行")
@pytest.mark.parametrize("file_path,originalPdf_path,excepted_result",load_test_data(csv_file_path))
@pytest.mark.api
def test_pdf_compare(common_headers,file_path,originalPdf_path,excepted_result):
    allure.step("检查json文件是否存在")
    if not os.path.exists(file_path):
        print(f"依赖的json文件路径{file_path}不存在")
    allure.step("检查pdf文件是否存在")
    if not os.path.exists(originalPdf_path):
        print(f"对比依赖的原pdf文件路径{originalPdf_path}不存在")
    compare_url = "https://c2.yonyoucloud.com/iuap-apcom-print/iuap-print-pdf/pdf/generate/compare"
    files = {
        'file':(os.path.basename(file_path),open(file_path,'rb')),
        'originalPdf':(os.path.basename(originalPdf_path),open(originalPdf_path,'rb'))
    }
    # 文件上传接口不能带 content-type: application/json，需移除，让 requests 自动设置 multipart/form-data
    upload_headers = {k: v for k, v in common_headers.items() if k.lower() != 'content-type'}
    try:
        logger.info(f"发送PDF对比请求，URL: {compare_url}")
        logger.info(f"文件1: {file_path}")
        logger.info(f"文件2: {originalPdf_path}")
        resu_response = requests.post(url=compare_url,files=files,headers=upload_headers,timeout=60)
        #time.sleep(3)
        # 验证HTTP状态码
        if resu_response.status_code != 200:
            pytest.fail(f"HTTP请求失败，状态码: {resu_response.status_code}, 响应内容: {resu_response.text[:200]}")

        content_type = resu_response.headers.get('Content-Type', '')
        logger.info(f"响应 Content-Type: {content_type}")
        if 'zip' not in content_type.lower() and 'octet-stream' not in content_type.lower():
            logger.error(f"预期ZIP类型响应，实际返回 Content-Type={content_type}，响应前200字符：{resu_response.text[:200]}")
            pytest.fail(f"预期ZIP类型响应，实际返回 Content-Type={content_type}")

        if len(resu_response.content) < 4 or not resu_response.content.startswith(b'PK'):
            snippet = resu_response.content[:256].decode('utf-8', errors='replace')
            pytest.fail(f"响应内容不是有效ZIP文件，前256字节：{snippet}")

        file_base = os.path.basename(file_path)
        # 去掉原有 .zip 后缀，避免生成 DYMB_001.zip.zip 双重后缀
        file_stem = file_base[:-4] if file_base.lower().endswith('.zip') else file_base
        # 保存到当前测试文件所在目录，避免污染项目根目录
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_zip_path = os.path.join(output_dir, f"temp_output_{file_stem}.zip")

        allure.step("保存响应数据到本地文件")
        logger.info("保存响应数据到本地文件")
        logger.info(f"HTTP状态码: {resu_response.status_code}")
        logger.info(f"响应内容长度: {len(resu_response.content)}")
        with open(output_zip_path,'wb') as f:
            f.write(resu_response.content)
            logger.info(f"响应数据已保存到: {output_zip_path}")

        allure.step(f"提取{file_path}的对比result结果")
        logger.info(f"提取{file_path}的对比result结果")
        with zipfile.ZipFile(output_zip_path,'r') as zip_f:
            if "result.txt" not in zip_f.namelist():
                pytest.fail("结果ZIP包中缺少 result.txt")
            with zip_f.open('result.txt') as res:
                content = res.read().decode('utf-8')
                logger.info(f"result.txt内容: {content[:500]}")
                if excepted_result in content:
                    assert True
                else:
                    pytest.fail(f'Expected {excepted_result} not found in result.txt')

    except zipfile.BadZipFile as bad_zip_err:
        pytest.fail(f"BadZipFile: {bad_zip_err}, 可能接口返回内容非ZIP或传输破损")
    except HTTPError as http_err:
        pytest.fail(f"HTTP error: {http_err}")
    except Exception as err:
        pytest.fail(f"Error: {err}")
    finally:
        # 关闭文件句柄
        for file_tuple in files.values():
            if hasattr(file_tuple[1], 'close'):
                file_tuple[1].close()