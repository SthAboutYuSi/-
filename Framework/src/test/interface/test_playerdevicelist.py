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

class TestDeviceList(unittest.TestCase):
	"""查询用户常用设备列表接口"""
	API_URL = Config().get('OpenPlatform_API').get('User2').get('DeviceList')
	excel = DATA_PATH + '/OpenPlatform_Player.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_DeviceList01(self):
		"""简单验证查询用户常用设备列表接口容错"""
		datas = ExcelReader(self.excel,sheet='UserSearch').data
		for d in range(0,len(datas)):
			if datas[d]['is_execute'] == 'N':
				continue
			else:
				with self.subTest(data=datas[d]['CaseNo']+datas[d]['describe']):
					self.setUp()
					# logger.debug(datas[d])
					expect = json.loads(ast.literal_eval(json.dumps(datas[d]['expection'])))
					casename = str(datas[d]['describe'])
					caseNo = str(datas[d]['CaseNo'])
					#请求的参数剔除期望值列、是否执行列、描述列、用例编号列
					datas[d].pop('expection')
					datas[d].pop('is_execute')
					datas[d].pop('describe')
					datas[d].pop('CaseNo')
					params = datas[d]			
					res = self.client.send(params=params)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					res_message = JMESPathExtractor().extract(query='message', body=res.text)
					res_error = JMESPathExtractor().extract(query='error', body=res.text)
					res_code = JMESPathExtractor().extract(query='code', body=res.text)
					responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
					res_data = JMESPathExtractor().extract(query='data', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
					if 'message' in expect.keys():
						self.assertEqual(expect['message'], res_message, msg=msg)
					if 'error' in expect.keys():
						self.assertEqual(expect['error'], res_error, msg=msg)	
					self.assertEqual(expect['code'], res_code, msg=msg)
					if 'data' in expect.keys() and expect['data']:
						self.assertEqual(expect['data'], res_data, msg=msg)	
					self.tearDown()



if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestDeviceList('test_DeviceList01'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)