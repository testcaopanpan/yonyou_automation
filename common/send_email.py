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


def send_email(report_path):
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
    msg['Subject'] = "自动化测试报告"

    # 添加邮件正文
    body = "自动化测试已完成，请查看附件中的测试报告"
    msg.attach(MIMEText(body, 'plain'))

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