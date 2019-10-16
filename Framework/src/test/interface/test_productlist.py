# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-29 09:35:04
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-16 17:17:51

import requests,unittest,os,sys,time,json,ast

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

class TestProductList(unittest.TestCase):
	"""产品列表接口"""
	API_URL = Config().get('OpenPlatform_API').get('Product').get('ProductList')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		self.mid = OpenPlatformCommon.getmid()
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_ProductList01(self):
		"""简单验证产品列表接口容错"""
		datas = ExcelReader(self.excel,sheet='ProductList').data
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
					if datas[d]['MerchantId'] == '{mid}':
						datas[d]['MerchantId'] = self.mid

					#转换为json格式
					# json.dumps(datas[d]['settings'])
					params = datas[d]
					# logger.debug(type(params))
					
					res = self.client.send(params=params)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.data[0].qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知错误', str(message),msg=msg)
					self.tearDown()

	def test_ProductList02(self):
		"""验证产品列表-产品名称搜索"""
		pid = OpenPlatformCommon.getpid(self.mid, category=2, platform=1)
		params = {'MerchantId': self.mid, 'Condition': 'Autotest测试', 'PageIndex': 1, 'PageSize': 1}
		res = self.client.send(params=params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_pid = JMESPathExtractor().extract(query='data.data[0].productId', body=res.text)
		res_pname = JMESPathExtractor().extract(query='data.data[0].productName', body=res.text)
		res_iconurl = JMESPathExtractor().extract(query='data.data[0].iconUrl', body=res.text)
		res_pnum = JMESPathExtractor().extract(query='data.data[0].productNum', body=res.text)
		res_pcategory = JMESPathExtractor().extract(query='data.data[0].productCategory', body=res.text)
		res_psubcategory = JMESPathExtractor().extract(query='data.data[0].subCategory', body=res.text)
		res_pecology = JMESPathExtractor().extract(query='data.data[0].productEcology', body=res.text)
		res_pmname = JMESPathExtractor().extract(query='data.data[0].merchantName', body=res.text)
		res_department = JMESPathExtractor().extract(query='data.data[0].department', body=res.text)
		res_pstate = JMESPathExtractor().extract(query='data.data[0].state', body=res.text)
		res_recordsTotal = JMESPathExtractor().extract(query='data.recordsTotal', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text

		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		self.assertEqual(pid, res_pid, msg=msg)
		self.assertEqual('Autotest测试', res_pname, msg=msg)
		self.assertIn('key=Autotest', str(res_iconurl), msg=msg)
		self.assertEqual(2, res_pcategory, msg=msg)
		self.assertEqual('单网页形态', res_psubcategory, msg=msg)
		self.assertEqual(0, res_pecology, msg=msg)
		self.assertEqual('中顺网络公司', res_pmname, msg=msg)
		self.assertEqual('Web研发部门', res_department, msg=msg)
		self.assertEqual(1, res_pstate, msg=msg)
		self.assertEqual(1, res_recordsTotal, msg=msg)

	def test_ProductList03(self):
		"""验证异常：产品列表-关键字匹配不到数据"""
		pid = OpenPlatformCommon.getpid(self.mid, category=2, platform=1)
		params = {'MerchantId': self.mid, 'Condition': 'Autotest测试12', 'PageIndex': 1, 'PageSize': 1}
		res = self.client.send(params=params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		# res_pid = JMESPathExtractor().extract(query='data.data[0].productId', body=res.text)
		# res_pname = JMESPathExtractor().extract(query='data.data[0].productName', body=res.text)
		# res_iconurl = JMESPathExtractor().extract(query='data.data[0].iconUrl', body=res.text)
		# res_pnum = JMESPathExtractor().extract(query='data.data[0].productNum', body=res.text)
		# res_pcategory = JMESPathExtractor().extract(query='data.data[0].productCategory', body=res.text)
		# res_psubcategory = JMESPathExtractor().extract(query='data.data[0].subCategory', body=res.text)
		# res_pecology = JMESPathExtractor().extract(query='data.data[0].productEcology', body=res.text)
		# res_pmname = JMESPathExtractor().extract(query='data.data[0].merchantName', body=res.text)
		# res_department = JMESPathExtractor().extract(query='data.data[0].department', body=res.text)
		# res_pstate = JMESPathExtractor().extract(query='data.data[0].state', body=res.text)
		res_recordsTotal = JMESPathExtractor().extract(query='data.recordsTotal', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text

		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertNotIn('未知错误', str(message),msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		# self.assertEqual(pid, res_pid, msg=msg)
		# self.assertEqual('Autotest测试', res_pname, msg=msg)
		# self.assertIn('key=Autotest', str(res_iconurl), msg=msg)
		# self.assertEqual(2, res_pcategory, msg=msg)
		# self.assertEqual('单网页形态', res_psubcategory, msg=msg)
		# self.assertEqual(0, res_pecology, msg=msg)
		# self.assertEqual('中顺网络公司', res_pmname, msg=msg)
		# self.assertEqual('Web研发部门', res_department, msg=msg)
		# self.assertEqual(1, res_pstate, msg=msg)
		self.assertEqual(0, res_recordsTotal, msg=msg)

	def test_ProductList04(self):
		"""验证产品列表-产品ID搜索"""
		pid = OpenPlatformCommon.getpid(self.mid, category=2, platform=1)
		params = {'MerchantId': self.mid, 'Condition': pid, 'PageIndex': 1, 'PageSize': 1}
		res = self.client.send(params=params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_pid = JMESPathExtractor().extract(query='data.data[0].productId', body=res.text)
		res_pname = JMESPathExtractor().extract(query='data.data[0].productName', body=res.text)
		res_iconurl = JMESPathExtractor().extract(query='data.data[0].iconUrl', body=res.text)
		res_pnum = JMESPathExtractor().extract(query='data.data[0].productNum', body=res.text)
		res_pcategory = JMESPathExtractor().extract(query='data.data[0].productCategory', body=res.text)
		res_psubcategory = JMESPathExtractor().extract(query='data.data[0].subCategory', body=res.text)
		res_pecology = JMESPathExtractor().extract(query='data.data[0].productEcology', body=res.text)
		res_pmname = JMESPathExtractor().extract(query='data.data[0].merchantName', body=res.text)
		res_department = JMESPathExtractor().extract(query='data.data[0].department', body=res.text)
		res_pstate = JMESPathExtractor().extract(query='data.data[0].state', body=res.text)
		res_recordsTotal = JMESPathExtractor().extract(query='data.recordsTotal', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text

		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		self.assertEqual(pid, res_pid, msg=msg)
		self.assertEqual('Autotest测试', res_pname, msg=msg)
		self.assertIn('key=Autotest', str(res_iconurl), msg=msg)
		self.assertEqual(2, res_pcategory, msg=msg)
		self.assertEqual('单网页形态', res_psubcategory, msg=msg)
		self.assertEqual(0, res_pecology, msg=msg)
		self.assertEqual('中顺网络公司', res_pmname, msg=msg)
		self.assertEqual('Web研发部门', res_department, msg=msg)
		self.assertEqual(1, res_pstate, msg=msg)
		self.assertEqual(1, res_recordsTotal, msg=msg)

	def test_ProductList05(self):
		"""验证产品列表-商户名称搜索"""
		pid = OpenPlatformCommon.getpid(self.mid, category=2, platform=1)
		params = {'MerchantId': self.mid, 'Condition': "中顺网络公司", 'PageIndex': 1, 'PageSize': 1}
		res = self.client.send(params=params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_pid = JMESPathExtractor().extract(query='data.data[0].productId', body=res.text)
		res_pname = JMESPathExtractor().extract(query='data.data[0].productName', body=res.text)
		res_iconurl = JMESPathExtractor().extract(query='data.data[0].iconUrl', body=res.text)
		res_pnum = JMESPathExtractor().extract(query='data.data[0].productNum', body=res.text)
		res_pcategory = JMESPathExtractor().extract(query='data.data[0].productCategory', body=res.text)
		res_psubcategory = JMESPathExtractor().extract(query='data.data[0].subCategory', body=res.text)
		res_pecology = JMESPathExtractor().extract(query='data.data[0].productEcology', body=res.text)
		res_pmname = JMESPathExtractor().extract(query='data.data[0].merchantName', body=res.text)
		res_department = JMESPathExtractor().extract(query='data.data[0].department', body=res.text)
		res_pstate = JMESPathExtractor().extract(query='data.data[0].state', body=res.text)
		res_recordsTotal = JMESPathExtractor().extract(query='data.recordsTotal', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text

		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		self.assertEqual(pid, res_pid, msg=msg)
		self.assertEqual('Autotest测试', res_pname, msg=msg)
		self.assertIn('key=Autotest', str(res_iconurl), msg=msg)
		self.assertEqual(2, res_pcategory, msg=msg)
		self.assertEqual('单网页形态', res_psubcategory, msg=msg)
		self.assertEqual(0, res_pecology, msg=msg)
		self.assertEqual('中顺网络公司', res_pmname, msg=msg)
		self.assertEqual('Web研发部门', res_department, msg=msg)
		self.assertEqual(1, res_pstate, msg=msg)
		self.assertEqual(1, res_recordsTotal, msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestProductList('test_ProductList01'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)