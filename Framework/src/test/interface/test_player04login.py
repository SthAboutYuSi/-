# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-08-09 15:38:07
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-29 11:05:54
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

class TestPlayerLogin(unittest.TestCase):
	"""玩家登录接口"""
	API_URL = Config().get('OpenPlatform_API').get('Player').get('Login')
	excel = DATA_PATH + '/OpenPlatform_Player.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_PlayerLogin01(self):
		"""批量验证玩家登录接口容错"""
		datas = ExcelReader(self.excel,sheet='Login').data
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
					res_data = JMESPathExtractor().extract(query='data', body=res.text)
					res_openId = JMESPathExtractor().extract(query='data.openId', body=res.text)
					res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
					res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
					res_mobile = JMESPathExtractor().extract(query='data.mobile', body=res.text)
					res_picture = JMESPathExtractor().extract(query='data.picture', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
					self.assertEqual(expect['success'], res_success, msg=msg)
					if 'message' in expect.keys():
						self.assertEqual(expect['message'], res_message, msg=msg)
					if 'error' in expect.keys():
						self.assertEqual(expect['error'], res_error, msg=msg)
					self.assertEqual(expect['code'], res_code, msg=msg)
					if 'data' in expect.keys() and expect['data']:
						self.assertEqual(expect['data']['openId'], res_openId, msg=msg)
						self.assertEqual(expect['data']['account'], res_account, msg=msg)
						self.assertEqual(expect['data']['nickname'], res_nickname, msg=msg)
						self.assertEqual(expect['data']['mobile'],res_mobile, msg=msg)
						# self.assertIsNotNone(res_picture, msg=msg)
						
					self.tearDown()

	def test_PlayerLogin02(self):
		"""验证手机验证码登录：单个在有效期内的验证码"""
		mobile = 17712345678
		code = OpenPlatformCommon.get_smscode(mobile=mobile)
		datas = {"channelNo": 81026962, "packageNo": 81026962001, "type": 1, "ip": "58.63.60.71", "machineCode": "s0qO3Jz9TLeM2CtQ50x", "appId": "8102Fv0aBOMJ5lbt6mMSrqBSPE7cpI8A", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": mobile, "SmsKey": "1", "SmsCode": code}, "networkState": 0, "wifiName": "MISnet"}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params,headers=headers)
		res_success = JMESPathExtractor().extract(query='success', body=res.text)
		res_message = JMESPathExtractor().extract(query='message', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		res_code = JMESPathExtractor().extract(query='code', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		res_openId = JMESPathExtractor().extract(query='data.openId', body=res.text)
		res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
		res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
		res_mobile= JMESPathExtractor().extract(query='data.mobile', body=res.text)
		res_picture = JMESPathExtractor().extract(query='data.picture', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertTrue(res_success, msg=msg)
		self.assertIsNone(res_error, msg=msg)
		self.assertEqual(0, res_code, msg=msg)
		self.assertEqual('jpSeis_Pz8_Pz8_Hzs_NxsrHyMiHu76v', res_openId, msg=msg)
		self.assertEqual('游客23113470', res_nickname, msg=msg)
		self.assertEqual(str(mobile), res_account, msg=msg)
		self.assertEqual(str(mobile), res_mobile, msg=msg)

	def test_PlayerLogin03(self):
		"""验证手机验证码登录：多个在有效期内验证码，输入最新的"""
		mobile = 17712345678
		code1 = OpenPlatformCommon.get_smscode(mobile=mobile)
		code2 = OpenPlatformCommon.get_smscode(mobile=mobile)
		datas = {"channelNo": 81026962, "packageNo": 81026962001, "type": 1, "ip": "58.63.60.71", "machineCode": "s0qO3Jz9TLeM2CtQ50x", "appId": "8102Fv0aBOMJ5lbt6mMSrqBSPE7cpI8A", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": mobile, "SmsKey": "1", "SmsCode": code2}, "networkState": 0, "wifiName": "MISnet"}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params,headers=headers)
		res_success = JMESPathExtractor().extract(query='success', body=res.text)
		res_message = JMESPathExtractor().extract(query='message', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		res_code = JMESPathExtractor().extract(query='code', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		res_openId = JMESPathExtractor().extract(query='data.openId', body=res.text)
		res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
		res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
		res_mobile= JMESPathExtractor().extract(query='data.mobile', body=res.text)
		res_picture = JMESPathExtractor().extract(query='data.picture', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertTrue(res_success, msg=msg)
		self.assertIsNone(res_error, msg=msg)
		self.assertEqual(0, res_code, msg=msg)
		self.assertEqual('jpSeis_Pz8_Pz8_Hzs_NxsrHyMiHu76v', res_openId, msg=msg)
		self.assertEqual('游客23113470', res_nickname, msg=msg)
		self.assertEqual(str(mobile), res_account, msg=msg)
		self.assertEqual(str(mobile), res_mobile, msg=msg)

	def test_PlayerLogin04(self):
		"""验证手机验证码登录：验证码超出有效期（2分钟）"""
		mobile = 17712345678
		code = OpenPlatformCommon.get_smscode(mobile=mobile)
		time.sleep(120)
		datas = {"channelNo": 81026962, "packageNo": 81026962001, "type": 1, "ip": "58.63.60.71", "machineCode": "s0qO3Jz9TLeM2CtQ50x", "appId": "8102Fv0aBOMJ5lbt6mMSrqBSPE7cpI8A", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": mobile, "SmsKey": "1", "SmsCode": code}, "networkState": 0, "wifiName": "MISnet"}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params,headers=headers)
		res_success = JMESPathExtractor().extract(query='success', body=res.text)
		res_message = JMESPathExtractor().extract(query='message', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		res_code = JMESPathExtractor().extract(query='code', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertFalse(res_success, msg=msg)
		self.assertEqual('验证码已过期',res_error, msg=msg)
		self.assertEqual(5, res_code, msg=msg)
		self.assertIsNone(res_data, msg=msg)

	def test_PlayerLogin05(self):
		"""验证手机验证码注册：有效期内多次请求验证码，输入的不是最新的"""
		mobile = 17712345678
		code1 = OpenPlatformCommon.get_smscode(mobile=mobile)
		code2 = OpenPlatformCommon.get_smscode(mobile=mobile)
		datas = {"channelNo": 81026962, "packageNo": 81026962001, "type": 1, "ip": "58.63.60.71", "machineCode": "s0qO3Jz9TLeM2CtQ50x", "appId": "8102Fv0aBOMJ5lbt6mMSrqBSPE7cpI8A", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": mobile, "SmsKey": "1", "SmsCode": code1}, "networkState": 0, "wifiName": "MISnet"}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params,headers=headers)
		res_success = JMESPathExtractor().extract(query='success', body=res.text)
		res_message = JMESPathExtractor().extract(query='message', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		res_code = JMESPathExtractor().extract(query='code', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertFalse(res_success, msg=msg)
		self.assertEqual('验证码错误',res_error, msg=msg)
		self.assertEqual(10, res_code, msg=msg)
		self.assertIsNone(res_data, msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestPlayerLogin('test_PlayerLogin04'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)