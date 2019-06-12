import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from src.utils.config import Config,DRIVER_PATH,DATA_PATH,REPORT_PATH
from src.utils.log import logger
from src.utils.file_reader import ExcelReader
from src.utils.HTMLTestRunner import HTMLTestRunner
from src.utils.mail import Email
from src.test.page.QKA_login_page import LoginPage
from src.test.page.QKA_home_page import HomePage

class TestLoginout(unittest.TestCase):
	"""登录登出测试"""
	URL = Config().get('URL')
	def setUp(self):
		self.page = LoginPage(browser_type='chrome').get(self.URL)
	def sub_tearDown(self):
		self.page.quit()
	def test_login(self):
		#输入用户名、密码、验证码，点击登录	
		self.page.set_username('admin')
		self.page.set_password('qkatest')
		self.page.set_code('123456')
		self.page.click_login
		WebDriverWait(self.page,10).until(EC.presence_of_element_located(self.page.defaulttab),'1-登录失败')
		#验证登录的用户名是否为‘admin’,不等于将抛出异常
		now_user=self.page.find_element_by_xpath('//*[@id="header-nav"]/ul/li[4]/a/span').text

		if now_user=='admin':
			print('登录成功！')
		else:
			raise NameError('用户名错误！')