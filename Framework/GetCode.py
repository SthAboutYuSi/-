from locust import HttpLocust, TaskSet, task
import queue,csv
from src.utils.extractor import JMESPathExtractor

class WebsiteTasks(TaskSet):

	# @task(1)
	# def test_getcode(self):
	# 	try:
	# 		data = self.locust.user_data_queue.get()
	# 	except queue.Empty:
	# 		print('uid data run out,test ended.')
	# 		exit(0)
		
	# 	payload = {
	# 		'uid': data['uid'],
	# 		"key":'booms啦啦啦',
	# 		"type": 0
	# 	}
	# 	res = self.client.post('/api/GameCode/GetCode',json=payload)
	# 	res_data = JMESPathExtractor().extract(query='data', body=res.text)
	# 	res_code = JMESPathExtractor().extract(query='code', body=res.text)
	# 	if res.status_code ==200:
	# 		if res_code == 0 and len(res_data) > 0:
	# 			print('GetCode with uid: {}'.format(data['uid']))
	# 		else:
	# 			print('GetCode Fail with uid: {}'.format(data['uid']))
	# 	else:
	# 		print('请求失败 with uid: {}'.format(data['uid']))


	@task(1)
	def test_exchangecode(self):
		try:
			data = self.locust.user_data_queue.get()
			code =  self.locust.code_data_queue.get()
		except queue.Empty:
			print('code data run out,test ended.')
			exit(0)
		
		payload = {
			'userId': data['uid'],
			'exchangeCode': code[0],
			'channelNO': 6000001001,
			'regChannelNO': 6000001001
		}
		print(payload)
		res = self.client.post('/api/ExchangeCode/Exchange',catch_response = True,json=payload)
		print(res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		res_code = JMESPathExtractor().extract(query='code', body=res.text)
		if res.status_code ==200:
			if res_code == 0 and len(res_data) > 0:
				print('GetCode with uid: {}'.format(data['uid']))
				res.success()
			else:
				print('GetCode Fail with uid: {}'.format(data['uid']))
				res.failure('error')
		else:
			print('请求失败 with uid: {}'.format(data['uid']))
			res.failure('error')


class WebsiteUser(HttpLocust):
	"""docstring for WebsiteUser"""
	task_set = WebsiteTasks
	# host = "http://172.16.6.242:8066"
	user_data_queue = queue.Queue()
	for index in range(100):
		data = {
			"uid": "%04d" % index
		}
		user_data_queue.put_nowait(data)
	code_data_queue = queue.Queue()
	with open('codedata.csv', encoding='utf-8')as f:
		codedata = csv.reader(f)
		for row in codedata:
			code_data_queue.put_nowait(row)
	min_wait = 1000
	max_wait = 3000

if __name__ == '__main__':
	import os
	os.system("locust -f GetCode.py --host=http://172.16.6.242:8066")
		