import allure
import pytest
from selenium.webdriver.common.keys import Keys

from pages.search_page import SearchPage
from pages.results_page import ResultsPage
from utils import switch_layout


@allure.feature('Search suggestions tests')
class TestSearchSuggestions:

    @pytest.fixture()
    def search_page(self, driver):
        page = SearchPage(driver).open()
        return page

    @allure.story('Suggestions for one word')
    @pytest.mark.parametrize('pattern', ['т', 'тест', 'test', 'ТЕСТ', '420', '=', ' test'],
                             ids=['one letter', 'cyrillic', 'latin', 'UPPERCASE', 'digits', 'symbol', 'with space'])
    def test_one_word(self, search_page, pattern):
        search_page.input_search(pattern)
        suggestions = search_page.get_suggestions()
        expected_result = pattern.lower().strip()
        for suggestion in suggestions:
            assert expected_result in suggestion.text or switch_layout(expected_result) in suggestion.text

    @allure.story('Suggestions for multiple words')
    @pytest.mark.parametrize('pattern', ['monty python', 'ьщтен python'],
                             ids=['exact match', 'wrong layout'])
    def test_multiple_words(self, search_page, pattern):
        search_page.input_search(pattern)
        suggestions = search_page.get_suggestions()
        expected_result = 'monty python'
        for suggestion in suggestions:
            assert expected_result in suggestion.text or switch_layout(expected_result) in suggestion.text

    @allure.story('Suggestions for part of well known phrase')
    def test_part_of_phrase(self, search_page):
        search_page.input_search('monty circ')
        suggestions = search_page.get_suggestions()
        results = [suggest.text for suggest in suggestions]
        assert 'monty python\'s flying circus' in results

    @allure.story('Placeholder suggestion')
    def test_inline_suggest(self, search_page):
        search_page.input_search('pyth')
        search_page.wait_text(search_page.INLINE_SUGGEST, 'python')
        search_page.go_to_results()
        ResultsPage(search_page._driver).get_results()
        assert 'python' in search_page.title.lower()

    @allure.story('Changing search field text due to suggestion selection')
    @pytest.mark.parametrize('key', [Keys.DOWN, Keys.UP], ids=['down', 'up'])
    def test_select_suggest_with_key(self, search_page, key):
        search_page.input_search('pyth')
        selected = search_page.navigate_over_suggestions(key)
        search_text = search_page.search_field_value()
        assert search_text == selected.text

    @allure.story('Go to results from suggestion selected by arrow key')
    def test_to_results_by_arrow(self, search_page):
        search_page.input_search('pyth')
        search_text = search_page.navigate_over_suggestions(Keys.DOWN).text
        search_page.get_element(search_page.SEARCH_FIELD).submit()
        ResultsPage(search_page._driver).get_results()
        assert search_text in search_page.title

    @allure.story('Go to results from suggestion selected by click')
    def test_to_results_by_click(self, search_page):
        search_page.input_search('pyth')
        suggestion = search_page.get_suggestions()[0]
        search_text = suggestion.text
        suggestion.click()
        ResultsPage(search_page._driver).get_results()
        assert search_text in search_page.title

    @allure.story('No results by forbidden words')
    def test_adult(self, search_page):
        search_page.input_search('porn')
        assert not search_page._driver.find_elements(*search_page.SUGGESTIONS)

    @allure.story('Suggestion changes by characters removing')
    def test_remove_characters(self, search_page):
        search_field = search_page.input_search('mail')
        first_suggestions = [suggestion.text for suggestion in search_page.get_suggestions()]
        search_field.send_keys(Keys.BACKSPACE + Keys.BACKSPACE)
        search_page.wait_text(search_page.INLINE_SUGGEST, 'ma')
        second_suggestions = [suggestion.text for suggestion in search_page.get_suggestions()]
        assert second_suggestions != first_suggestions
