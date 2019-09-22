import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ResultsPage(BasePage):
    RESULTS = (By.CLASS_NAME, 'result')

    @allure.step("get results")
    def get_results(self):
        return self.get_element(self.RESULTS)
