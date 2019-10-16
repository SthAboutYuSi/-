# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-08-09 15:38:07
# @Last Modified by:   yusi
# @Last Modified time: 2019-08-23 10:13:39
import requests,unittest,os,sys,time,json,ast

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
# print (sys.path)
from src.utils.config import Config,DATA_PATH,REPORT_PATH
from src.utils.log import logger
from src.utils.file_reader import ExcelReader
from src.utils.HTMLTestReportCN import HTMLTestRunner
from src.utils.client import HTTPClient
from src.utils.extractor import JMESPathExtractor
from src.test.common.OpenPlatformCommon import OpenPlatformCommon

class TestPlayerPromote(unittest.TestCase):
	"""玩家转正接口"""
	API_URL = Config().get('OpenPlatform_API').get('Player').get('Promote')
	excel = DATA_PATH + '/OpenPlatform_Player.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_PlayerPromote01(self):
		"""批量验证玩家转正接口容错"""
		datas = ExcelReader(self.excel,sheet='Promote').data
		for d in range(0,len(datas)):
			if datas[d]['is_execute'] == 'N':
				continue
			else:
				with self.subTest(data=datas[d]['CaseNo']+datas[d]['describe']):
					self.setUp()
					# logger.debug(datas[d])
					expect = json.loads(ast.literal_eval(json.dumps(datas[d]['expection'])))
					# expect = datas[d]['expection']
					# logger.debug(expect)
					# logger.debug(type(expect))
					casename = str(datas[d]['describe'])
					caseNo = str(datas[d]['CaseNo'])
					#请求的参数剔除期望值列、是否执行列、描述列、用例编号列
					datas[d].pop('expection')
					datas[d].pop('is_execute')
					datas[d].pop('describe')
					datas[d].pop('CaseNo')

					datas[d]['payload'] = ast.literal_eval(datas[d]['payload'])
					params = json.dumps(datas[d])
					# logger.debug(type(params))
					headers={'Content-Type': "application/json"}
					res = self.client.send(data=params,headers=headers)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					res_success = JMESPathExtractor().extract(query='success', body=res.text)
					res_message = JMESPathExtractor().extract(query='message', body=res.text)
					res_error = JMESPathExtractor().extract(query='error', body=res.text)
					res_code = JMESPathExtractor().extract(query='code', body=res.text)
					responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
					self.assertEqual(expect['success'], res_success, msg=msg)
					if 'message' in expect.keys():
						self.assertEqual(expect['message'], res_message, msg=msg)
					if 'error' in expect.keys():
						self.assertEqual(expect['error'], res_error, msg=msg)
					self.assertEqual(expect['code'], res_code, msg=msg)

					self.tearDown()

	def test_PlayerPromote02(self):
		"""验证手机验证码转正：单个在有效期内的验证码"""
		if OpenPlatformCommon.get_registinfo() != '注册失败':
			openId = OpenPlatformCommon.get_registinfo()['openId']
			unionId = OpenPlatformCommon.get_registinfo()['unionId']
			nickname = OpenPlatformCommon.get_registinfo()['nickname']
			account = OpenPlatformCommon.get_registinfo()['account']
			password = OpenPlatformCommon.get_registinfo()['password']
			mobile = 13225757037
			code = OpenPlatformCommon.get_smscode(mobile=mobile)
			datas = {"openId": openId, "packageNo": 81036962002, "type": 1, "payload": {"mobile": mobile, "smsKey": "1", "smsCode": code, "password": "TestCase2"}}
			params = json.dumps(datas)
			headers={'Content-Type': "application/json"}
			res = self.client.send(data=params,headers=headers)
			res_success = JMESPathExtractor().extract(query='success', body=res.text)
			res_message = JMESPathExtractor().extract(query='message', body=res.text)
			res_error = JMESPathExtractor().extract(query='error', body=res.text)
			res_code = JMESPathExtractor().extract(query='code', body=res.text)
			responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
			msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
			self.assertTrue(res_success, msg=msg)
			self.assertIsNone(res_error, msg=msg)
			self.assertEqual(0, res_code, msg=msg)

	def test_PlayerPromote03(self):
		"""验证手机验证码转正：多个在有效期内验证码，输入最新的"""
		if OpenPlatformCommon.get_registinfo() != '注册失败':
			openId = OpenPlatformCommon.get_registinfo()['openId']
			unionId = OpenPlatformCommon.get_registinfo()['unionId']
			nickname = OpenPlatformCommon.get_registinfo()['nickname']
			account = OpenPlatformCommon.get_registinfo()['account']
			password = OpenPlatformCommon.get_registinfo()['password']
			mobile = 13225757099
			code1 = OpenPlatformCommon.get_smscode(mobile=mobile)
			code2 = OpenPlatformCommon.get_smscode(mobile=mobile)
			datas = {"openId": openId, "packageNo": 81036962002, "type": 1, "payload": {"mobile": mobile, "smsKey": "1", "smsCode": code2, "password": "TestCase2"}}
			params = json.dumps(datas)
			headers={'Content-Type': "application/json"}
			res = self.client.send(data=params,headers=headers)
			res_success = JMESPathExtractor().extract(query='success', body=res.text)
			res_message = JMESPathExtractor().extract(query='message', body=res.text)
			res_error = JMESPathExtractor().extract(query='error', body=res.text)
			res_code = JMESPathExtractor().extract(query='code', body=res.text)
			responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
			msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
			self.assertTrue(res_success, msg=msg)
			self.assertIsNone(res_error, msg=msg)
			self.assertEqual(0, res_code, msg=msg)

	def test_PlayerPromote04(self):
		"""验证手机验证码转正：验证码超出有效期（2分钟）"""
		if OpenPlatformCommon.get_registinfo() != '注册失败':
			openId = OpenPlatformCommon.get_registinfo()['openId']
			unionId = OpenPlatformCommon.get_registinfo()['unionId']
			nickname = OpenPlatformCommon.get_registinfo()['nickname']
			account = OpenPlatformCommon.get_registinfo()['account']
			password = OpenPlatformCommon.get_registinfo()['password']
			mobile = 13225757199
			code = OpenPlatformCommon.get_smscode(mobile=mobile)
			time.sleep(120)
			datas = {"openId": openId, "packageNo": 81036962002, "type": 1, "payload": {"mobile": mobile, "smsKey": "1", "smsCode": code, "password": "TestCase2"}}
			params = json.dumps(datas)
			headers={'Content-Type': "application/json"}
			res = self.client.send(data=params,headers=headers)
			res_success = JMESPathExtractor().extract(query='success', body=res.text)
			res_message = JMESPathExtractor().extract(query='message', body=res.text)
			res_error = JMESPathExtractor().extract(query='error', body=res.text)
			res_code = JMESPathExtractor().extract(query='code', body=res.text)
			responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
			msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
			self.assertFalse(res_success, msg=msg)
			self.assertEqual('验证短信失败',res_error, msg=msg)
			self.assertEqual(10, res_code, msg=msg)

	def test_PlayerPromote05(self):
		"""验证手机验证码转正：有效期内多次请求验证码，输入的不是最新的"""
		if OpenPlatformCommon.get_registinfo() != '注册失败':
			openId = OpenPlatformCommon.get_registinfo()['openId']
			unionId = OpenPlatformCommon.get_registinfo()['unionId']
			nickname = OpenPlatformCommon.get_registinfo()['nickname']
			account = OpenPlatformCommon.get_registinfo()['account']
			password = OpenPlatformCommon.get_registinfo()['password']
			mobile = 19925757299
			code1 = OpenPlatformCommon.get_smscode(mobile=mobile)
			code2 = OpenPlatformCommon.get_smscode(mobile=mobile)
			datas = {"openId": openId, "packageNo": 81036962002, "type": 1, "payload": {"mobile": mobile, "smsKey": "1", "smsCode": code1, "password": "TestCase2"}}
			params = json.dumps(datas)
			headers={'Content-Type': "application/json"}
			res = self.client.send(data=params,headers=headers)
			res_success = JMESPathExtractor().extract(query='success', body=res.text)
			res_message = JMESPathExtractor().extract(query='message', body=res.text)
			res_error = JMESPathExtractor().extract(query='error', body=res.text)
			res_code = JMESPathExtractor().extract(query='code', body=res.text)
			responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
			msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
			self.assertFalse(res_success, msg=msg)
			self.assertEqual('验证短信失败',res_error, msg=msg)
			self.assertEqual(10, res_code, msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestPlayerPromote('test_PlayerPromote01'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)
