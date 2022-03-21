from .basepage import BasePage
from selenium.webdriver.common.by import By
from librapage.home_page import HomePage


class CenterPage(BasePage):
    title = "中台系统"
    libra_home = (By.CSS_SELECTOR, ".enter-name")

    def enter_libra_home(self):
        self.click(self.libra_home)
        return HomePage(self.driver)
