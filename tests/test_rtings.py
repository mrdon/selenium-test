import selenium
from selenium import webdriver
import pytest
from time import sleep
import polling
import pages
from functools import wraps
import inspect


@pytest.fixture(scope="module")
def browser():
    options = webdriver.ChromeOptions()
    result = webdriver.Chrome(options=options)
    try:
        yield result
    finally:
        result.quit()


def screenshot(func):
    @wraps(func)
    def wrapper(browser, *args, **kwargs):
        try:    
            return func(browser, *args, **kwargs)
        except Exception as e:
            f = inspect.getfile(func).split("/")[-1][:-3]
            browser.get_screenshot_as_file(f"/tmp/{f}_{func.__name__}.png")
            raise e
        
    return wrapper


@screenshot
def test_has_results(browser):
    home = pages.Homepage(browser)
    items = home.search("HS 60").results
    assert len(items) >= 10


@screenshot 
def test_has_no_results(browser):
    home = pages.Homepage(browser)
    search = home.search("asdfasdf")
    assert search.no_results
     
