from selenium.webdriver.common.by import By
from src.test.common.page import Page


class LoginPage(Page):
	"""登录页面"""
	#页面元素定义
	#用户名
    useraccount = (By.ID, "txt_account")
    #密码
    userpassword = (By.ID, "txt_password")
    #手机验证码
    msgcode = (By.ID, "txt_code")
    #登录按钮
    loginbutton = (By.ID, "login_button")

    #定位用户名输入框，清空输入框内容再输入用户名
    def set_username(self, username):
        name = self.find_element(*self.useraccount)
        name.clear()
        name.send_keys(username)

    # 定位密码输入框，清空输入框内容再输入密码 
    def set_password(self,password):
    	pwd = self.find_element(*self.userpassword)
    	pwd.clear()
    	pwd.send_keys(password)

    #定位验证码输入框，清空输入框内容再输入验证码
	def set_code(self,code):
    	code = self.find_element(*self.msgcode)
    	code.clear()
    	code.send_keys(code)

    #定位登录按钮并点击
    def click_login(self):
    	okbtn=self.find_element(*self.loginbutton)
    	okbtn.click()