# _*_ coding:utf-8 _*_
# common/__init__.py

# 导入常用模块
from .logger import logger
from .base_page import BasePage
from .send_email import send_email

# 定义包的公开接口
__all__ = ['logger', 'BasePage', 'send_email']