from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ex_cond
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    URL = "https://go.mail.ru"

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    @property
    def title(self):
        return self._driver.title

    def navigate_to(self, url):
        self._driver.get(url)

    def open(self):
        self.navigate_to(self.URL)
        return self

    def get_element(self, locator: tuple, timeout=5) -> WebElement:
        return WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_element_located(locator), ' : '.join(locator))

    def get_elements(self, locator: tuple, timeout=5) -> List[WebElement]:
        return WebDriverWait(self._driver, timeout).until(
            ex_cond.visibility_of_any_elements_located(locator), ' : '.join(locator))

    def wait_text(self, locator: tuple, text: str, timeout=5) -> WebElement:
        return WebDriverWait(self._driver, timeout).until(
            ex_cond.text_to_be_present_in_element(locator, text), ' : '.join(locator))
