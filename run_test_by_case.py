# _*_ coding:utf-8 _*_
import pytest
import sys,os
from datetime import datetime
from common.logger import logger
from common.send_email import send_email


def main():
    test_case_list = [
        "test_cases/test_ui/test_ui_template_list.py::test_print_template_search",
        "test_cases/test_ui/test_ui_template_list.py::test_search_lingyujieidan",
        "test_cases/test_ui/test_ui_template_list.py::test_kongjian_list_drag_default_value"
    ]
    #构建pytest命令行参数
    pytest_avg = []
    for path in test_case_list:
        #检查径是否存在
        if "::" in path:
            #检查包含用例名称的路径是否存在
            file_path,test_case_name = path.split("::",1)
            if os.path.exists(file_path):
                pytest_avg.append(path)
            else:
                print(f"该路径{file_path}不存在，跳过该路径用例")
        else:
            if os.path.exists(path):
                pytest_avg.append(path)
            else:
                print(f"该路径{path}不存在，跳过该路径用例")
    #如果没有指定运行的测试用例，则执行如下默认路径的全量用例
    if not pytest_avg:
        pytest_avg = ["test_cases"]
    #配置报告路径等内容
    report_name = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_dir = 'reports'
    report_path = os.path.join(report_dir, report_name)
    #配置过程log
    logg = logger
    logg.info(f"执行 pytest，参数：{pytest_avg}")
    # 添加 pytest 配置
    pytest_avg.extend([
        "-v",  # 显示详细的测试结果
        "--tb=short",  # 简化错误信息
        "--html=" + report_path,  # 生成 HTML 测试报告
        "--self-contained-html",  # 生成独立的 HTML 测试报告
        "--maxfail=5",  # 最多允许 5 个测试用例失败
        "--timeout=300",  # 设置每个测试用例的超时时间为 300 秒
        "--no-header",  # 不显示 pytest 版本信息
        "--no-summary",  # 不显示测试结果摘要
    ])
    # 执行 pytest
    try:
        pytest.main(pytest_avg)
    except Exception as e:
        print(f"执行 pytest 时出错：{e}")
        sys.exit(1)
   # send_email = send_email()
    #send_email.send_report()


if __name__ == "__main__":
    main()
