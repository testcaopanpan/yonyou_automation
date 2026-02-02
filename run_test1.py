# _*_ coding:utf-8 _*_
# run_test.py

import pytest
import os
from datetime import datetime
import argparse
import logging
from common.send_email import send_email

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# 执行测试
def run_test(test_case=None, report_path=None):
    try:
        # 创建测试报告目录
        if not report_path:
            report_dir = 'reports'
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)

            # 生成测试报告文件名
            report_name = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            report_path = os.path.join(report_dir, report_name)

        # 执行测试并生成测试报告
        pytest_args = [
            '-v',
            '--html=' + report_path,
            '--self-contained-html'
        ]

        if test_case:
            pytest_args.append(test_case)

        pytest.main(pytest_args)

        logger.info(f"测试报告已生成: {report_path}")

        # 发送测试报告
        send_email(report_path)
    except Exception as e:
        logger.error(f"执行测试失败: {e}")


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='执行自动化测试')
    parser.add_argument('--test_case', help='指定测试用例')
    parser.add_argument('--report_path', help='指定测试报告路径')
    args = parser.parse_args()

    # 执行测试
    run_test(args.test_case, args.report_path)