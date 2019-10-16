# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-08-09 15:38:07
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-27 19:27:21
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

class TestPlayerRegist(unittest.TestCase):
	"""玩家注册接口"""
	API_URL = Config().get('OpenPlatform_API').get('Player').get('Regist')
	excel = DATA_PATH + '/OpenPlatform_Player.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_PlayerRegist01(self):
		"""批量验证玩家注册接口容错"""
		datas = ExcelReader(self.excel,sheet='Regist').data
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
					res_unionId = JMESPathExtractor().extract(query='data.unionId', body=res.text)
					res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
					res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
					res_password = JMESPathExtractor().extract(query='data.password', body=res.text)
					res_picture = JMESPathExtractor().extract(query='data.picture', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
					self.assertEqual(expect['success'], res_success, msg=msg)
					if 'message' in expect.keys():
						self.assertEqual(expect['message'], res_message, msg=msg)
					if 'error' in expect.keys():
						self.assertEqual(expect['error'], res_error, msg=msg)
					self.assertEqual(expect['code'], res_code, msg=msg)
					if 'data' in expect.keys() and expect['data']:
						self.assertGreater(len(res_openId), 0, msg=msg)
						self.assertGreater(len(res_unionId), 0, msg=msg)
						self.assertIn('游客', res_nickname, msg=msg)
						if datas[d]['type'] == 2:
							mobile = datas[d]['payload']['Mobile']
							self.assertEqual(mobile, res_account, msg=msg)
						else:
							self.assertEqual(10, len(res_account), msg=msg)
						self.assertEqual(18, len(res_password), msg=msg)
						# self.assertIsNotNone(res_picture, msg=msg)
						
					self.tearDown()

	def test_PlayerRegist02(self):
		"""验证手机验证码注册：单个在有效期内的验证码"""
		mobile = 19925757088
		code = OpenPlatformCommon.get_smscode(mobile=mobile)
		datas = {"type": 2, "channelNo": 81026962, "packageNo": 81026962001, "ip": "58.63.60.133", "machineCode": "autotest8888", "appId": "8103xqzESJOPvBzwHikLWwTXHfF6iZzE", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": mobile, "SmsKey": "1", "SmsCode": code}, "networkState": 0, "wifiName": "MISnet"}
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
		res_unionId = JMESPathExtractor().extract(query='data.unionId', body=res.text)
		res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
		res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
		res_password = JMESPathExtractor().extract(query='data.password', body=res.text)
		res_picture = JMESPathExtractor().extract(query='data.picture', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertTrue(res_success, msg=msg)
		self.assertIsNone(res_error, msg=msg)
		self.assertEqual(0, res_code, msg=msg)
		self.assertGreater(len(res_openId), 0, msg=msg)
		self.assertGreater(len(res_unionId), 0, msg=msg)
		self.assertIn('游客', res_nickname, msg=msg)
		self.assertEqual(str(mobile), res_account, msg=msg)
		self.assertEqual(18, len(res_password), msg=msg)

	def test_PlayerRegist03(self):
		"""验证手机验证码注册：多个在有效期内验证码，输入最新的"""
		mobile = 19925757099
		code1 = OpenPlatformCommon.get_smscode(mobile=mobile)
		code2 = OpenPlatformCommon.get_smscode(mobile=mobile)
		datas = {"type": 2, "channelNo": 81026962, "packageNo": 81026962001, "ip": "58.63.60.133", "machineCode": "autotest8888", "appId": "8103xqzESJOPvBzwHikLWwTXHfF6iZzE", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": mobile, "SmsKey": "1", "SmsCode": code2}, "networkState": 0, "wifiName": "MISnet"}
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
		res_unionId = JMESPathExtractor().extract(query='data.unionId', body=res.text)
		res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
		res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
		res_password = JMESPathExtractor().extract(query='data.password', body=res.text)
		res_picture = JMESPathExtractor().extract(query='data.picture', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertTrue(res_success, msg=msg)
		self.assertIsNone(res_error, msg=msg)
		self.assertEqual(0, res_code, msg=msg)
		self.assertGreater(len(res_openId), 0, msg=msg)
		self.assertGreater(len(res_unionId), 0, msg=msg)
		self.assertIn('游客', res_nickname, msg=msg)
		self.assertEqual(str(mobile), res_account, msg=msg)
		self.assertEqual(18, len(res_password), msg=msg)

	def test_PlayerRegist04(self):
		"""验证手机验证码注册：验证码超出有效期（2分钟）"""
		mobile = 19925757199
		code = OpenPlatformCommon.get_smscode(mobile=mobile)
		time.sleep(120)
		datas = {"type": 2, "channelNo": 81026962, "packageNo": 81026962001, "ip": "58.63.60.133", "machineCode": "autotest8888", "appId": "8103xqzESJOPvBzwHikLWwTXHfF6iZzE", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": mobile, "SmsKey": "1", "SmsCode": code}, "networkState": 0, "wifiName": "MISnet"}
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
		res_unionId = JMESPathExtractor().extract(query='data.unionId', body=res.text)
		res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
		res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
		res_password = JMESPathExtractor().extract(query='data.password', body=res.text)
		res_picture = JMESPathExtractor().extract(query='data.picture', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertFalse(res_success, msg=msg)
		self.assertEqual('手机验证码错误',res_error, msg=msg)
		self.assertEqual(10, res_code, msg=msg)
		self.assertIsNone(res_data, msg=msg)

	def test_PlayerRegist05(self):
		"""验证手机验证码注册：有效期内多次请求验证码，输入的不是最新的"""
		mobile = 19925757299
		code1 = OpenPlatformCommon.get_smscode(mobile=mobile)
		code2 = OpenPlatformCommon.get_smscode(mobile=mobile)
		datas = {"type": 2, "channelNo": 81026962, "packageNo": 81026962001, "ip": "58.63.60.133", "machineCode": "autotest8888", "appId": "8103xqzESJOPvBzwHikLWwTXHfF6iZzE", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": mobile, "SmsKey": "1", "SmsCode": code1}, "networkState": 0, "wifiName": "MISnet"}
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
		res_unionId = JMESPathExtractor().extract(query='data.unionId', body=res.text)
		res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
		res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
		res_password = JMESPathExtractor().extract(query='data.password', body=res.text)
		res_picture = JMESPathExtractor().extract(query='data.picture', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertFalse(res_success, msg=msg)
		self.assertEqual('手机验证码错误',res_error, msg=msg)
		self.assertEqual(10, res_code, msg=msg)
		self.assertIsNone(res_data, msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestPlayerRegist('test_PlayerRegist05'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)
	# a='{"success": true,"code": 0,"error": null,"responseTime": "2019-08-08 17:34:19.140","data": {"a":1}}'
	# b= json.dumps(a)
	# c=ast.literal_eval(b)
	# d= json.loads(c)
	# if d['data']:
	# 	print('data不为空')
	# else:
	# 	print('data为空')


	
	# # m={"type": 2, "channelNo": 81026962, "packageNo": 81026962001, "ip": "59.41.117.126", "machineCode": "yr0k464luy1c", "appId": "8103xqzESJOPvBzwHikLWwTXHfF6iZzE", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {"Mobile": "19925757037", "SmsKey": "1", "SmsCode": "666666"}, "networkState": 0, "wifiName": "MISnet"}
	# # print(m['type'],type(m['type']))
	# print(a,type(a))
	# print(b,type(b))
	# print(c,type(c))
	# print(d,type(d))
	# # print(if d['data'],type(d['data']))
	# if 'error' in d.keys():
	# 	print ('d]')
	# if 'message' in d.keys():
	# 	print("message")