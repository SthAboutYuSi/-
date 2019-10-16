# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-22 18:41:27
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-10 17:24:31
import requests,unittest,os,sys,time,json

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
# print (sys.path)
from src.utils.config import Config,DATA_PATH,REPORT_PATH
from src.utils.log import logger
from src.utils.file_reader import ExcelReader
from src.utils.HTMLTestReportCN import HTMLTestRunner
from src.utils.mail import Email
from src.utils.client import HTTPClient
from src.utils.extractor import JMESPathExtractor
from src.test.common.OpenPlatformCommon import OpenPlatformCommon
from src.utils.generator import random_password,random_name

class TestAdminAdd(unittest.TestCase):
	"""管理员创建接口"""
	API_URL = Config().get('OpenPlatform_API').get('Admin').get('AdminAdd')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		self.mid = OpenPlatformCommon.getmid()
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_AdminAdd01(self):
		"""简单验证新增管理员接口容错"""
		datas = ExcelReader(self.excel,sheet='AddAdmin').data
		for d in range(0,len(datas)):
			if datas[d]['is_execute'] == 'N':
				continue
			else:
				with self.subTest(data=datas[d]['CaseNo']+datas[d]['describe']):
					self.setUp()
					# logger.debug(datas[d])
					expect = datas[d]['expect_code']
					casename = str(datas[d]['describe'])
					caseNo = str(datas[d]['CaseNo'])
					#请求的参数剔除期望值列、是否执行列、描述列、用例编号列
					datas[d].pop('expect_code')
					datas[d].pop('is_execute')
					datas[d].pop('describe')
					datas[d].pop('CaseNo')
					if datas[d]['mid'] == '{mid}':
						datas[d]['mid'] = self.mid

					if datas[d]['loginAccount'] == '{str+num}':
						datas[d]['loginAccount'] = random_password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
					elif datas[d]['loginAccount'] == '{str}':
						datas[d]['loginAccount'] = random_password(length=10, special_chars=False, digits=False, upper_case=True, lower_case=True)
					elif datas[d]['loginAccount'] == '{num}':
						datas[d]['loginAccount'] = random_password(length=10, special_chars=False, digits=True, upper_case=False, lower_case=False)
					elif datas[d]['loginAccount'] == '{long}':
						datas[d]['loginAccount'] = random_password(length=100, special_chars=False, digits=True, upper_case=True, lower_case=True)
					elif datas[d]['loginAccount'] == '{chinese}':
						datas[d]['loginAccount'] = random_name()

					#转换为json格式
					params = json.dumps(datas[d])
					# logger.debug(type(params))
					headers={'Content-Type': "application/json"}
					res = self.client.send(data=params,headers=headers)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知错误', str(message),msg=msg)
					self.tearDown()

	def test_AdminAdd02(self):
		"""验证添加成功后返回是否正确"""
		account = random_password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
		datas = {"mid": self.mid, "loginAccount": account, "loginPassword": "ccccS001", "verifyPassword": "ccccS001", "position": "", "realName": "", "roleId": 1, "state": 1}
		headers={'Content-Type': "application/json"}

		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		res = self.client.send(data=json.dumps(datas),headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_aid = JMESPathExtractor().extract(query='data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + json.dumps(datas) + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(res.text),msg=msg)
		self.assertIn(date, str(responseTime),msg=msg)
		self.assertEqual(32, len(res_aid),msg=msg)

	def test_AdminAdd03(self):
		"""验证异常-同一商户新建2个商户管理员"""
		account1 = random_password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
		account2 = random_password(length=9, special_chars=False, digits=True, upper_case=True, lower_case=True)
		data1 = {"mid": self.mid, "loginAccount": account1, "loginPassword": "ccccS001", "verifyPassword": "ccccS001", "position": "", "realName": "", "roleId": 1, "state": 1}
		data2 = {"mid": self.mid, "loginAccount": account2, "loginPassword": "ccccS001", "verifyPassword": "ccccS001", "position": "", "realName": "", "roleId": 1, "state": 1}
		headers={'Content-Type': "application/json"}
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		self.client.send(data=json.dumps(data1),headers=headers)
		res = self.client.send(data=json.dumps(data2),headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		# res_aid = JMESPathExtractor().extract(query='data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + json.dumps(data2) + '\n返回结果:' + res.text
		self.assertEqual('false', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(res.text),msg=msg)
		self.assertIn(date, str(responseTime),msg=msg)
		self.assertIsNone(res_data, msg=msg)
		# self.assertEqual(32, len(res_aid),msg=msg)

	def test_AdminAdd04(self):
		"""验证异常-新建同名管理员"""
		account = random_password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
		data = {"mid": self.mid, "loginAccount": account, "loginPassword": "ccccS001", "verifyPassword": "ccccS001", "position": "", "realName": "", "roleId": 1, "state": 1}		
		headers={'Content-Type': "application/json"}
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		self.client.send(data=json.dumps(data),headers=headers)
		res = self.client.send(data=json.dumps(data),headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + json.dumps(data) + '\n返回结果:' + res.text
		self.assertEqual('false', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(res.text),msg=msg)
		self.assertIn(date, str(responseTime),msg=msg)
		self.assertEqual('该账号已存在!', res_error, msg=msg)
		self.assertIsNone(res_data, msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestAdminAdd('test_AdminAdd04'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)