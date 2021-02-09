import pytest
import polling
from typing import List
from selene.api import browser, s, ss


class SearchResults:

    @property
    def results(self) -> List[str]:

        def get_items():
            return ss(".searchbar_results-name")

        items = polling.poll(get_items, step=0.1, timeout=5)
        return [item.text for item in items]

    @property
    def no_results(self) -> bool:

        def get_items():
            return s(".searchbar_results-empty").is_displayed()

        polling.poll(get_items, step=0.1, timeout=5)
        return True
      
 
class Homepage:
    def __init__(self):
        browser.open_url("https://rtings.com")

    def search(self, text) -> SearchResults:
        search = s("input[data-node='search_input']")
        search.send_keys(f"{text}\n")
        return SearchResults()




