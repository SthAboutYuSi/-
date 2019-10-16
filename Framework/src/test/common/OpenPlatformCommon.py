import os,sys,json
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
from src.utils.config import Config
from src.utils.client import HTTPClient
from src.utils.extractor import JMESPathExtractor
from src.utils.generator import random_password,random_name
from src.utils.DBoperator import MYSQL

class OpenPlatformCommon():
	"""开放平台公共函数"""

	def getmid():
		"""获取商户id"""
		datas = {"name": "中顺网络公司", "shortName": "ZS棋牌", "type": 1, "state": 1, "principal": "中顺棋牌", "creditCode": "91440106589536704F", "legalRepresentative": "李石头", "mobile": "39956888", "address": "广东省广州市天河区天河软件园建中路50号多玩游戏大厦4楼", "contactName": "王小姐", "contactMobile": 19978953221, "email": "ZS@qq.com", "qq": 54321, "weChat": "qkagame", "businessLicense": "20190722/953ba822fb8643b282e6102712d96c24.jpg", "classicalChinese": "20190722/c5e60fd2961b97aca2ea3ec735892a40.jpg", "icp": "20190722/056fa26e44814b1ea36b288df9523f2f.jpeg", "corporateIdentityCard": "20190722/9fc2f9a61ae8486084f69ea6393f637d.jpeg"}
		headers={'Content-Type': "application/json"}
		url = Config().get('OpenPlatform_API').get('Merchant').get('MerchantCreate')
		client = HTTPClient(url=url, method='POST')
		res = client.send(data=json.dumps(datas),headers=headers)
		mid = JMESPathExtractor().extract(query='data', body=res.text)
		return mid

	def getmcode(mid):
		"""获取商户编号,商户名称，商户简称，商户类型，商户状态"""
		params = {"id": mid}
		url = Config().get('OpenPlatform_API').get('Merchant').get('MerchantGet')
		client = HTTPClient(url=url, method='GET')
		res = client.send(params=params)
		mcode = JMESPathExtractor().extract(query='data.code', body=res.text)
		mname = JMESPathExtractor().extract(query='data.name', body=res.text)
		mshortname = JMESPathExtractor().extract(query='data.shortName', body=res.text)
		#返回的商户类型
		mtype = JMESPathExtractor().extract(query='data.type', body=res.text)
		#返回的商户类型名称
		mtypename = JMESPathExtractor().extract(query='data.typeName', body=res.text)
		#返回的商户状态值
		mstate = JMESPathExtractor().extract(query='data.state', body=res.text)
		#返回的商户状态
		mstatename = JMESPathExtractor().extract(query='data.stateName', body=res.text)
		#返回的商户主体
		mprincipal = JMESPathExtractor().extract(query='data.principal', body=res.text)
		#返回的社会统一信用码
		mcreditcode = JMESPathExtractor().extract(query='data.creditCode', body=res.text)
		#返回的法人信息
		mlegalrepresentative = JMESPathExtractor().extract(query='data.legalRepresentative', body=res.text)
		return mcode,mname,mshortname,mtype,mtypename,mstate,mstatename

	def getaid(mid):
		"""获取管理员id, 传入的登录账户名"""
		account = random_password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
		datas = {"mid": mid, "loginAccount": account, "loginPassword": "Aotutest1", "verifyPassword": "Aotutest1", "position": "", "operator": "", "realName": "", "roleId": 3, "state": 1}
		headers={'Content-Type': "application/json"}
		url = Config().get('OpenPlatform_API').get('Admin').get('AdminAdd')
		client = HTTPClient(url=url, method='POST')
		res = client.send(data=json.dumps(datas),headers=headers)
		aid = JMESPathExtractor().extract(query='data', body=res.text)
		return aid, account

	def getpid(mid, category=1, platform=0):
		""" -----获取产品id-----
		参数-mid：所属商户id
		参数-category：产品类型 1-APP 2-H5 3-小程序
		参数-platform：产品APP平台 0-安卓 1-苹果
		"""
		datas = {"merchantId": mid,"introduction": "Autotest自动化自动创建产品","name": "Autotest测试","department": "Web研发部门","ecology": 0,"iconUrl": "Autotest","category": category,"state": 1,"setting": {"platform": platform,"packageName": "Autotest","signature": "Autotest","bundleID": "Autotest.bundleID","appId": "Autotest.appId","h5Type": 0,"h5PlatformName": "AutotestH5","h5Address": "Autotest.H5","smallProgramId": "AutotestsmallProgramId","smallPlatformType": 0}}
		headers={'Content-Type': "application/json"}
		url = Config().get('OpenPlatform_API').get('Product').get('Product')
		client = HTTPClient(url=url, method='POST')
		res = client.send(data=json.dumps(datas),headers=headers)
		pid = JMESPathExtractor().extract(query='data', body=res.text)

		return pid

	def getcid():
		""" -----获取渠道id-----
		
		"""
		datas = {"name": "Autotest渠道测试","type": 1,"developerPlatform":"Autotest开发者平台"}
		headers={'Content-Type': "application/json"}
		url = Config().get('OpenPlatform_API').get('Channel').get('ChannelCreate')
		client = HTTPClient(url=url, method='POST')
		res = client.send(data=json.dumps(datas),headers=headers)
		cid = JMESPathExtractor().extract(query='data', body=res.text)

		return cid

	def get_smscode(mobile):
		""" -----获取手机验证码-----
		
		"""
		datas = {"sesskey": "1","mobile": mobile,"imgVerifyCode": "string","smsProvider": 0}
		headers={'Content-Type': "application/json"}
		url = Config().get('OpenPlatform_API').get('VerifyCode').get('sms')
		client = HTTPClient(url=url, method='POST')
		res = client.send(data=json.dumps(datas),headers=headers)
		if JMESPathExtractor().extract(query='success', body=res.text):
			msg = JMESPathExtractor().extract(query='error', body=res.text)
		else:
			msg = "获取验证码失败"
		return msg

	def get_registinfo():
		""" -----获取游客注册信息-----
		
		"""
		datas = {"type": 1, "channelNo": 81036962, "packageNo": 81036962001, "ip": "59.41.117.126", "machineCode": "AotutestRegister", "appId": "8103xqzESJOPvBzwHikLWwTXHfF6iZzE", "terminalType": 1, "osVersion": "Android.8.3.1", "machineModel": "MI 9", "payload": {}, "networkState": 0, "wifiName": "MISnet"}
		headers={'Content-Type': "application/json"}
		url = Config().get('OpenPlatform_API').get('Player').get('Regist')
		client = HTTPClient(url=url, method='POST')
		res = client.send(data=json.dumps(datas),headers=headers)
		if JMESPathExtractor().extract(query='success', body=res.text):
			# res_openId = JMESPathExtractor().extract(query='data.openId', body=res.text)
			# res_unionId = JMESPathExtractor().extract(query='data.unionId', body=res.text)
			# res_nickname = JMESPathExtractor().extract(query='data.nickname', body=res.text)
			# res_account = JMESPathExtractor().extract(query='data.account', body=res.text)
			# res_password = JMESPathExtractor().extract(query='data.password', body=res.text)
			msg = JMESPathExtractor().extract(query='data', body=res.text)
		else:
			msg = "注册失败"
		return msg

if __name__ == '__main__':
	a=OpenPlatformCommon.getcid()
	print(a,type(a))
	# a= '#+AAQkX_QcyWDEZGiMyvyvoZ_I9&PCGrky2He2oA^)0zv8Es5#bF7sqz!IH1G5x3dYnuH6ouu%eMHRShP9CK6ng&$CfFIWV6jv&lgRZ4eVlOUwe#cu&qF3wXbtJcr__No*6uCYNrDXTGUsZhzQ8@avTRX^ssV5ODf5H$(ym56&ezc78jSzlffKlyzESm+i6rLmT(JYx1f^!y^aq*N+TEdtMiklxP+M8yCLC+xiORSWGQcQ)h!hMmFPm+PGHMwfMYO'
	# print(len(a))