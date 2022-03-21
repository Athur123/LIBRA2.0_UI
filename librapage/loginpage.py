import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from librapage.basepage import BasePage
from librapage.centerpage import CenterPage


class LoginPage(BasePage):
    title: str = "中台系统"
    login_name = (By.CSS_SELECTOR, '.login-pc [formcontrolname="loginName"]')
    user_name = (By.CSS_SELECTOR, '.login-pc [formcontrolname="userName"]')
    user_passwd = (By.CSS_SELECTOR, '.login-pc [formcontrolname="password"]')
    submit = (By.CSS_SELECTOR, '.login-pc .ant-btn-primary')
    error_message = (By.CSS_SELECTOR, '.login-pc .ant-notification .ant-notification-notice-message')

    def enter_login_name(self, loginname: str) -> None:
        self.type(self.login_name, loginname)

    def enter_user_name(self, username: str) -> None:
        self.type(self.user_name, username)

    def enter_user_passwd(self, passwd: str) -> None:
        self.type(self.user_passwd, passwd)

    def get_error_message(self) -> str:
        return self.get_text(self.error_message)

    def login(self, loginname: str, username: str, passwd: str) -> CenterPage:
        self.enter_login_name(loginname)
        self.enter_user_name(username)
        self.enter_user_passwd(passwd)
        self.click(self.submit)

        return CenterPage(self.driver)
