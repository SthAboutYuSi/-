from selenium.webdriver.common.by import By
from src.test.common.page import Page

class HomePage(Page):  
    """主页"""  
  	#页面元素定义
    # 右上角用户个人菜单
    userdropdown = (By.XPATH, '//*[@id="header-nav"]/ul/li[4]/a')
    #登录用户名
    loginname = (By.XPATH,'//*[@id="header-nav"]/ul/li[4]/a/span')
    #个人菜单-安全退出选项
    outlogin = (By.LINK_TEXT,"安全退出")

    #menutab-平台介绍
    defaulttab = (By.LINK_TEXT,'平台介绍')

    #左侧菜单面板
    #个人中心
    usercenter = (By.XPATH,'//*[@id="sidebar-nav"]/ul/li[3]/a')


    #

 