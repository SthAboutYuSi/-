# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-08-23 15:07:55
# @Last Modified by:   yusi
# @Last Modified time: 2019-10-08 19:24:21
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

class TestDeviceSet(unittest.TestCase):
	"""设置用户常用设备接口"""
	API_URL = Config().get('OpenPlatform_API').get('User2').get('DeviceInfo')
	excel = DATA_PATH + '/OpenPlatform_Player.xlsx'

	def setUp(self):
		# self.client = HTTPClient(url=self.API_URL, method='POST')
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_DeviceSet01(self):
		"""批量验证设置用户常用设备接口容错"""
		datas = ExcelReader(self.excel,sheet='deviceNo').data
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
					playerId = datas[d]['playerId']
					#请求的参数剔除期望值列、是否执行列、描述列、用例编号列
					datas[d].pop('expection')
					datas[d].pop('is_execute')
					datas[d].pop('describe')
					datas[d].pop('CaseNo')
					datas[d].pop('playerId')
					datas[d]['deviceNo'] = ast.literal_eval(datas[d]['deviceNo'])
					url = "%s%s" %(self.API_URL,playerId)
					params = json.dumps(datas[d])
					# logger.debug(type(params))
					headers={'Content-Type': "application/json"}
					self.client = HTTPClient(url=url, method='POST')
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


if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestDeviceSet('test_DeviceSet01'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)