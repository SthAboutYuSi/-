import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.utils.config import Config,DRIVER_PATH,DATA_PATH,REPORT_PATH
from src.utils.log import logger
from src.utils.file_reader import ExcelReader
from src.utils.HTMLTestRunner import HTMLTestRunner
from src.utils.mail import Email
from src.test.page.baidu_result_page import BaiDuMainPage, BaiDuResultPage

class TestBaiDu(unittest.TestCase):
		
	URL = Config().get('URL')
	excel = DATA_PATH + '/baidu.xlsx'
     
	def sub_setUp(self):
		# 初始页面是main page，传入浏览器类型打开浏览器
		self.page = BaiDuMainPage(browser_type='chrome').get(self.URL, maximize_window=True)	
		#self.driver = webdriver.Chrome(executable_path=DRIVER_PATH+'\chromedriver.exe')
		#self.driver.get(self.URL)
	def sub_tearDown(self):
		#self.driver.quit()
		self.page.quit()
	def test_search(self):
		datas=ExcelReader(self.excel).data
		for d in datas:
			with self.subTest(data=d):
				self.sub_setUp()
				#self.driver.find_element(*self.locator_kw).send_keys(d['search'])
				#self.driver.find_element(*self.locator_su).click()
				self.page.search(d['search'])
				time.sleep(2)
				self.page = BaiDuResultPage(self.page)  # 页面跳转到result page
				links = self.page.result_links
				#links = self.driver.find_elements(*self.locator_result)
				for link in links:
					logger.info(link.text)
				self.sub_tearDown()
		

if __name__ == '__main__':
	#取当前时间
	now= time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
	#定义报告存放路径，支持相对路径
	report = os.path.join(REPORT_PATH , now + 'report.html')
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='搭建测试框架', description='修改html报告')
		runner.run(TestBaiDu('test_search'))
	e = Email(title = Config().get('email').get('title'),
              message = Config().get('email').get('message'),
              receiver = Config().get('email').get('receiver'),
              server = Config().get('email').get('server'),
              sender = Config().get('email').get('sender'),
              password = Config().get('email').get('password'),
              path = report
              )
	e.send()