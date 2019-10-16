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

class TestProductGet(unittest.TestCase):
	"""产品详情接口"""
	API_URL = Config().get('OpenPlatform_API').get('Product').get('Product')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		self.mid = OpenPlatformCommon.getmid()
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_ProductGet01(self):
		"""简单验证获取产品信息接口容错"""
		datas = ExcelReader(self.excel,sheet='ProductDetail').data
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
					if datas[d]['ProductId'] == '{pid}':
						datas[d]['ProductId'] = OpenPlatformCommon.getpid(self.mid)

					#转换为json格式
					# json.dumps(datas[d]['settings'])
					params = datas[d]
					# logger.debug(type(params))
					
					res = self.client.send(params=params)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知错误', str(message),msg=msg)
					self.tearDown()

	def test_ProductGet02(self):
		"""验证新增产品成功后获取产品信息是否正确"""
		pid = OpenPlatformCommon.getpid(self.mid)
		params = {"ProductId":pid}
		res = self.client.send(params=params)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + str(pid) + '\n返回结果:' + res.text
		#获取返回信息
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_pid = JMESPathExtractor().extract(query='data.productId', body=res.text)
		res_pname = JMESPathExtractor().extract(query='data.productName', body=res.text)
		res_iconurl = JMESPathExtractor().extract(query='data.iconUrl', body=res.text)
		res_pnum = JMESPathExtractor().extract(query='data.productNum', body=res.text)
		res_pcategory = JMESPathExtractor().extract(query='data.productCategory', body=res.text)
		res_pecology = JMESPathExtractor().extract(query='data.productEcology', body=res.text)
		res_pmname = JMESPathExtractor().extract(query='data.merchantName', body=res.text)
		res_department = JMESPathExtractor().extract(query='data.department', body=res.text)
		res_psecret =  JMESPathExtractor().extract(query='data.productSecret', body=res.text)
		res_pintroduction = JMESPathExtractor().extract(query='data.introduction', body=res.text)
		res_pstate = JMESPathExtractor().extract(query='data.state', body=res.text)
		res_psettings_platform = JMESPathExtractor().extract(query='data.settings.platform', body=res.text)
		res_psettings_packagename = JMESPathExtractor().extract(query='data.settings.packageName', body=res.text)
		res_psettings_signature = JMESPathExtractor().extract(query='data.settings.signature', body=res.text)
		res_psettings_bundleID = JMESPathExtractor().extract(query='data.settings.bundleID', body=res.text)
		res_psettings_appID = JMESPathExtractor().extract(query='data.settings.appId', body=res.text)
		res_psettings_h5type = JMESPathExtractor().extract(query='data.settings.h5Type', body=res.text)
		res_psettings_h5platformname = JMESPathExtractor().extract(query='data.settings.h5PlatformName', body=res.text)
		res_psettings_h5address = JMESPathExtractor().extract(query='data.settings.h5Address', body=res.text)
		res_psettings_smallProgramId = JMESPathExtractor().extract(query='data.settings.smallProgramId', body=res.text)
		res_psettings_smallPlatformType = JMESPathExtractor().extract(query='data.settings.smallPlatformType', body=res.text)
		
		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		self.assertEqual(pid, res_pid, msg=msg)
		self.assertEqual('Autotest测试', res_pname, msg=msg)
		self.assertIn('key=Autotest', str(res_iconurl), msg=msg)
		self.assertEqual(1, res_pcategory, msg=msg)
		self.assertEqual(0, res_pecology, msg=msg)
		self.assertEqual('中顺网络公司', res_pmname, msg=msg)
		self.assertEqual('Web研发部门', res_department, msg=msg)
		self.assertEqual('Autotest自动化自动创建产品', res_pintroduction, msg=msg)
		self.assertEqual(1, res_pstate, msg=msg)
		self.assertEqual(0, res_psettings_platform, msg=msg)
		self.assertEqual('Autotest', res_psettings_packagename, msg=msg)
		self.assertEqual('Autotest', res_psettings_signature, msg=msg)
		self.assertEqual('Autotest.bundleID', res_psettings_bundleID, msg=msg)
		self.assertEqual('Autotest.appId', res_psettings_appID, msg=msg)
		self.assertEqual(0, res_psettings_h5type, msg=msg)
		self.assertEqual('AutotestH5', res_psettings_h5platformname, msg=msg)
		self.assertEqual('Autotest.H5', res_psettings_h5address, msg=msg)
		self.assertEqual('AutotestsmallProgramId', res_psettings_smallProgramId, msg=msg)
		self.assertEqual(0,res_psettings_smallPlatformType, msg=msg)

	def test_ProductGet03(self):
		"""验证修改产品成功后获取产品信息是否正确"""
		pid = OpenPlatformCommon.getpid(self.mid)
		edit_datas = {"productId": pid, "name": "编辑产品名Autotest","iconUrl": "iconUrl.modify","department": "modify部门","introduction": "modify介绍","state": 2,"settings": {"packageName": "modify包名","signature": "modifysignature","bundleID": "modifybundleID","appId": "modifyAPPID", "h5PlatformName": "modifyH5平台名","h5Address": "modifyH5.Address","smallProgramId": "modifysmallProgramId"}}
		edit_url = Config().get('OpenPlatform_API').get('Product').get('Product')
		edit_headers = {'Content-Type': "application/json"}
		edit_client = HTTPClient(url=self.API_URL, method='PATCH')
		edit_client.send(data=json.dumps(edit_datas),headers=edit_headers)
		#查询编辑后的产品信息
		params = {"ProductId":pid}
		res = self.client.send(params=params)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + str(pid) + '\n返回结果:' + res.text
		#获取返回信息
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_pid = JMESPathExtractor().extract(query='data.productId', body=res.text)
		res_pname = JMESPathExtractor().extract(query='data.productName', body=res.text)
		res_iconurl = JMESPathExtractor().extract(query='data.iconUrl', body=res.text)
		res_pnum = JMESPathExtractor().extract(query='data.productNum', body=res.text)
		res_pcategory = JMESPathExtractor().extract(query='data.productCategory', body=res.text)
		res_pecology = JMESPathExtractor().extract(query='data.productEcology', body=res.text)
		res_pmname = JMESPathExtractor().extract(query='data.merchantName', body=res.text)
		res_department = JMESPathExtractor().extract(query='data.department', body=res.text)
		res_psecret =  JMESPathExtractor().extract(query='data.productSecret', body=res.text)
		res_pintroduction = JMESPathExtractor().extract(query='data.introduction', body=res.text)
		res_pstate = JMESPathExtractor().extract(query='data.state', body=res.text)
		res_psettings_platform = JMESPathExtractor().extract(query='data.settings.platform', body=res.text)
		res_psettings_packagename = JMESPathExtractor().extract(query='data.settings.packageName', body=res.text)
		res_psettings_signature = JMESPathExtractor().extract(query='data.settings.signature', body=res.text)
		res_psettings_bundleID = JMESPathExtractor().extract(query='data.settings.bundleID', body=res.text)
		res_psettings_appID = JMESPathExtractor().extract(query='data.settings.appId', body=res.text)
		res_psettings_h5type = JMESPathExtractor().extract(query='data.settings.h5Type', body=res.text)
		res_psettings_h5platformname = JMESPathExtractor().extract(query='data.settings.h5PlatformName', body=res.text)
		res_psettings_h5address = JMESPathExtractor().extract(query='data.settings.h5Address', body=res.text)
		res_psettings_smallProgramId = JMESPathExtractor().extract(query='data.settings.smallProgramId', body=res.text)
		res_psettings_smallPlatformType = JMESPathExtractor().extract(query='data.settings.smallPlatformType', body=res.text)
		
		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		self.assertEqual(pid, res_pid, msg=msg)
		self.assertEqual('编辑产品名Autotest', res_pname, msg=msg)
		self.assertIn('key=iconUrl.modify', str(res_iconurl), msg=msg)
		self.assertEqual(1, res_pcategory, msg=msg)
		self.assertEqual(0, res_pecology, msg=msg)
		self.assertEqual('中顺网络公司', res_pmname, msg=msg)
		self.assertEqual('modify部门', res_department, msg=msg)
		self.assertEqual('modify介绍', res_pintroduction, msg=msg)
		self.assertEqual(2, res_pstate, msg=msg)
		self.assertEqual(0, res_psettings_platform, msg=msg)
		self.assertEqual('modify包名', res_psettings_packagename, msg=msg)
		self.assertEqual('modifysignature', res_psettings_signature, msg=msg)
		self.assertEqual('modifybundleID', res_psettings_bundleID, msg=msg)
		self.assertEqual('modifyAPPID', res_psettings_appID, msg=msg)
		self.assertEqual(0, res_psettings_h5type, msg=msg)
		self.assertEqual('modifyH5平台名', res_psettings_h5platformname, msg=msg)
		self.assertEqual('modifyH5.Address', res_psettings_h5address, msg=msg)
		self.assertEqual('modifysmallProgramId', res_psettings_smallProgramId, msg=msg)
		self.assertEqual(0,res_psettings_smallPlatformType, msg=msg)




if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestProductGet('test_ProductGet03'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)