from locust import HttpLocust, TaskSet, task

class WebsiteTasks(TaskSet):
	"""docstring for WebsiteTasks"""
	def on_start(self):
		self.client.post("/login",{
		"username": "test",
		"password": "123456"
		})

	@task(2)
	def index(self):
		self.client.get("/")
	
	@task(1)
	def about(self):
		self.client.get("/about/")

class WebsiteUser(HttpLocust):
	"""docstring for WebsiteUser"""
	task_set = WebsiteTasks
	# host = "https//debugtalk.com"
	min_wait = 1000
	max_wait = 5000

if __name__ == '__main__':
	import os
	os.system("locust -f test.py --host=https://debugtalk.com")
		