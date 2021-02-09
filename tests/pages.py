import selenium
from selenium import webdriver
import pytest
import polling
from selenium.common.exceptions import NoSuchElementException
from typing import List


class SearchResults:
    def __init__(self, browser):
        self.browser = browser

    @property
    def results(self) -> List[str]:

        def get_items():
            try:
                return self.browser.find_elements_by_class_name("searchbar_results-name")
            except NoSuchElementException:
                return []

        items = polling.poll(get_items, step=0.1, timeout=5)
        return [item.text for item in items]

    @property
    def no_results(self) -> bool:

        def get_items():
            try:
                return self.browser.find_element_by_class_name("searchbar_results-empty").is_displayed()
            except NoSuchElementException:
                return False

        polling.poll(get_items, step=0.1, timeout=5)
        return True
      
 
class Homepage:
    def __init__(self, browser):
        self.browser = browser
        browser.get("https://rtings.com")

    def search(self, text) -> SearchResults:
        search = self.browser.find_element_by_xpath("//input[@data-node='search_input']")
        search.send_keys(f"{text}\n")
        return SearchResults(self.browser)

from selene.api import browser as selene_browser, s

class SeleneHomepage:
    def __init__(self):
        selene_browser.open_url("https://rtings.com")

    def search(self, text) -> SearchResults:
        search = s("input[data-node='search_input']")
        search.send_keys(f"{text}\n")
        return True # SearchResults(self.browser)




