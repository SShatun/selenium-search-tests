from random import randint

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from pages.results_page import ResultsPage


class SearchPage(BasePage):
    SEARCH_FIELD = (By.CLASS_NAME, 'pm-toolbar__search__input')
    SUGGESTIONS = (By.CLASS_NAME, "go-suggests__ellipsis")
    SELECTED_SUGGESTION = (By.CLASS_NAME, "go-suggests__item_select")
    SUGGESTIONS_BOLD = (By.XPATH, '//*[@class="go-suggests__ellipsis"]')
    INLINE_SUGGEST = (By.CLASS_NAME, 'input-inline-suggest')

    @allure.step("input string in search field {search_string}")
    def input_search(self, search_string: str):
        field = self.get_element(self.SEARCH_FIELD)
        field.send_keys(search_string)
        return field

    @allure.step("get search field text")
    def search_field_value(self):
        return self.get_element(self.SEARCH_FIELD).get_attribute("value")

    @allure.step("get list of suggestions")
    def get_suggestions(self):
        return self.get_elements(self.SUGGESTIONS)

    @allure.step("go to results page")
    def go_to_results(self):
        form = self.get_element(self.SEARCH_FIELD)
        form.send_keys(Keys.RIGHT)
        form.submit()
        return ResultsPage(self._driver)

    @allure.step("push arrows to navigate over suggestions")
    def navigate_over_suggestions(self, direction: Keys, times: int = None):
        suggestions = self.get_elements(self.SUGGESTIONS)
        times = times or randint(1, len(suggestions))
        search_field = self.get_element(self.SEARCH_FIELD)
        for push in range(times):
            search_field.send_keys(direction)
        return self.get_element(self.SELECTED_SUGGESTION)

