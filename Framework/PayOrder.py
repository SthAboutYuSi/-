from locust import HttpLocust, TaskSet, task
import queue,csv,time
from src.utils.extractor import JMESPathExtractor

class WebsiteTasks(TaskSet):

	@task(1)
	def test_pay(self):
		try:
			data = self.locust.user_data_queue.get()
		except queue.Empty:
			print('test ended.')
			exit(0)
		
		payload ={"merchantCode": "A00166598", "isPloy": 1, "platformType": 0, "orderNO": data['orderNO'], "amount": 1, "productId": 10000, "quantity": 100, "name": "金币", "desc": "100金币", "device": 4, "typeCode": "alipay", "extData": "", "extInfo": "", "openId": "jpSeis_Pz8_Pz8_Hzs_NzszKzcuxusyR", "appId": "", "notifyUrl": "http://www.baidu.com", "sign": "test", "signType": "RSA", "version": "1.0"}
		
		res = self.client.post('/pay',catch_response = True,json=payload)
		
		if res.status_code ==200:
			res_code = JMESPathExtractor().extract(query='code', body=res.text)
			if res_code == 0 :
				print('下单成功: {}'.format(data['orderNO']))
				res.success()
			else:
				print('下单失败: {}'.format(data['orderNO']))
				res.failure('fail')
				print(res.text)
		else:
			print('请求失败 with {}'.format(data['orderNO']))
			res.failure('error')



class WebsiteUser(HttpLocust):
	"""docstring for WebsiteUser"""
	task_set = WebsiteTasks
	# host = "http://172.16.6.242:8066"
	user_data_queue = queue.Queue()
	for index in range(2000):
		data = {
			"orderNO": str(int(time.time()*1000))+"%06d"  % index
		}
		user_data_queue.put_nowait(data)
	min_wait = 1000
	max_wait = 3000

if __name__ == '__main__':
	import os
	os.system("locust -f PayOrder.py --host=http://192.168.0.166:8099")