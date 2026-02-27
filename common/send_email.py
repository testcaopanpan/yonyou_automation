# _*_ coding:utf-8 _*_
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from common.logger import logger
import socket
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_junit_stats(junit_path):
    """
    解析 pytest --junitxml 结果，按 API / UI 统计：
    - total: 总用例数
    - executed: 执行用例数（总数 - skipped）
    - failed: 失败+错误 数
    - passed: 通过数
    - pass_rate: 通过率（0~1）
    """
    stats = {
        "api": {"total": 0, "executed": 0, "failed": 0, "passed": 0, "pass_rate": 0.0},
        "ui": {"total": 0, "executed": 0, "failed": 0, "passed": 0, "pass_rate": 0.0},
    }

    if not junit_path or not os.path.exists(junit_path):
        logger.warning(f"JUnit 报告不存在，路径：{junit_path}")
        return stats

    try:
        tree = ET.parse(junit_path)
        root = tree.getroot()

        if root.tag == "testsuite":
            suites = [root]
        elif root.tag == "testsuites":
            suites = root.findall("testsuite")
        else:
            suites = []

        # 先按 testcases 逐个统计，再汇总
        for suite in suites:
            for case in suite.findall("testcase"):
                classname = case.attrib.get("classname", "")  # 如 test_cases.test_ui.test_xxx
                name = case.attrib.get("name", "")
                nodeid = f"{classname}::{name}" if classname else name

                # 简单按路径区分 API / UI
                key = None
                if "test_api" in nodeid:
                    key = "api"
                elif "test_ui" in nodeid:
                    key = "ui"
                else:
                    continue  # 其它用例先不统计

                stats[key]["total"] += 1

                skipped_el = case.find("skipped")
                failure_el = case.find("failure")
                error_el = case.find("error")

                if skipped_el is not None:
                    # 跳过不计入 executed
                    continue

                # 走到这里说明是“真正执行”的
                stats[key]["executed"] += 1

                if failure_el is not None or error_el is not None:
                    stats[key]["failed"] += 1
                else:
                    stats[key]["passed"] += 1

        # 计算通过率
        for key in ("api", "ui"):
            executed = stats[key]["executed"]
            passed = stats[key]["passed"]
            stats[key]["pass_rate"] = (passed / executed) if executed > 0 else 0.0

    except Exception as e:
        logger.error(f"解析 JUnit 报告失败：{e}")

    return stats
def send_email(report_path,junit_path=None):
    # 邮件配置
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    sender_email = "957406615@qq.com"
    sender_password = "xzixxyujjsmwbfej"
    receiver_email = "957406615@qq.com"

    # 检查网络连接
    try:
        socket.create_connection((smtp_server, smtp_port), timeout=10)
        logger.info("网络连接正常")
    except Exception as e:
        logger.error(f"网络连接失败: {e}")
        return

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    # ====== 标题使用 当前日期时间 + 批次自动化测试已完成 ======
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg['Subject'] = f"{now_str} 批次自动化测试已完成"
    # ====== 根据 JUnit 统计生成正文 ======
    stats = parse_junit_stats(junit_path)
    api = stats["api"]
    ui = stats["ui"]

    body = f"""具体执行情况如下

    api：总用例数【{api['total']}】，执行用例数【{api['executed']}】，失败用例数【{api['failed']}】，通过用例数【{api['passed']}】，通过率为{api['pass_rate'] * 100:.2f}%；失败用例详情请前往执行服务器查看执行日志

    UI：总用例数【{ui['total']}】，执行用例数【{ui['executed']}】，失败用例数【{ui['failed']}】，通过用例数【{ui['passed']}】，通过率为{ui['pass_rate'] * 100:.2f}%；失败用例详情请前往执行服务器查看执行日志及失败截图
    """
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    # ====================================================

    # 添加附件
    if os.path.exists(report_path):
        with open(report_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(report_path)}')
        msg.attach(part)
    else:
        logger.error(f"测试报告文件不存在: {report_path}")
        return

    # 检查邮件内容大小
    if sys.getsizeof(msg.as_string()) > 10 * 1024 * 1024:
        logger.error("邮件内容过大")
        return

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        logger.info("测试报告邮件已发送")
    except Exception as e:
        logger.error(f"发送邮件失败: {str(e)}")