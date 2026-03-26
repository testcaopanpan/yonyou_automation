# _*_ coding:utf-8 _*_
# run_test.py

import pytest
import os
from datetime import datetime
import argparse
from common.send_email import send_email
from common.logger import logger

def run_api_test(report_path=None):
    '''
    该方法用于只跑api用例
    '''
    try:
        # 创建测试报告目录
        timestmp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not report_path:
            report_dir = 'reports'
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)

            # 生成测试报告文件名
            report_name = f"api_report_{datetime.now().strftime(timestmp)}.html"
            report_path = os.path.join(report_dir, report_name)

            # JUnit XML 报告（新加）
            junit_name = f"api_result_{timestmp}.xml"
            junit_path = os.path.join(report_dir, junit_name)
        # 执行测试并生成测试报告
        allure_dir = os.path.join("reports","allure_results","api"+timestmp)
        if not os.path.exists(allure_dir):
            os.makedirs(allure_dir)
        pytest_args = [
            "test_cases/test_api",
            "-m","api",
            "-n4",#自动执行并发
            "-v",
            f"--html={report_path}",
            "--self-contained-html",  # 这里末尾要有逗号
            f"--alluredir={allure_dir}",  # 这个是单独一个参数
            f"--junitxml={junit_path}", #生成junit结果
        ]
        logger.info(f"开始执行 pytest：{pytest_args}")
        exit_code = pytest.main(pytest_args)
        logger.info(f"pytest 执行结束，退出码：{exit_code}")
        # 发送测试报告
        send_email(report_path,junit_path)
    except Exception as e:
        logger.error(f"执行api测试失败: {e}")

def run_ui_test(report_path=None):
    '''
        该方法用于只跑api用例
        '''
    try:
        # 创建测试报告目录
        timestmp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not report_path:
            report_dir = 'reports'
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)

            # 生成测试报告文件名
            report_name = f"ui_report_{datetime.now().strftime(timestmp)}.html"
            report_path = os.path.join(report_dir, report_name)

            # JUnit XML 报告（新加）
            junit_name = f"ui_result_{timestmp}.xml"
            junit_path = os.path.join(report_dir, junit_name)
        # 执行测试并生成测试报告
        allure_dir = os.path.join("reports", "allure_results", "ui" + timestmp)
        if not os.path.exists(allure_dir):
            os.makedirs(allure_dir)
        pytest_args = [
            "test_cases/test_ui",
            "-m","ui",
            "-v",
            f"--html={report_path}",
            "--self-contained-html",  # 这里末尾要有逗号
            f"--alluredir={allure_dir}",  # 这个是单独一个参数
            f"--junitxml={junit_path}",  # 生成junit结果
        ]
        logger.info(f"开始执行 pytest：{pytest_args}")
        exit_code = pytest.main(pytest_args)
        logger.info(f"pytest 执行结束，退出码：{exit_code}")
        # 发送测试报告
        send_email(report_path, junit_path)
    except Exception as e:
        logger.error(f"执行ui测试失败: {e}")

# 执行测试
def run_all_test(report_path=None):
    run_ui_test(report_path)
    run_api_test(report_path)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='执行自动化测试')
    parser.add_argument('--test_case', help='指定测试用例')
    parser.add_argument('--type', choices=['api', 'ui', 'all'], default='all',
                        help='指定执行类型：api / ui / all')
    parser.add_argument('--report_path', help='指定测试报告路径')
    args = parser.parse_args()
    if args.type == "api":
        run_api_test(args.report_path)
    elif args.type =="ui":
        run_ui_test(args.report_path)
    else:
        run_all_test()