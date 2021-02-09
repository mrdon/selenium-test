import selene_pages as pages
import time
from functools import wraps
from selene.api import browser
import inspect

def screenshot(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:    
            return func(*args, **kwargs)
        except Exception as e:
            f = inspect.getfile(func).split("/")[-1][:-3]
            path = "/tmp"
            filename = f"{f}_{func.__name__}.png"
            print(f"Saved screenshot at {path}/{filename}")
            browser.take_screenshot(path=path, filename=filename)
            raise e
        
    return wrapper


@screenshot
def test_has_results():
    home = pages.Homepage()
    items = home.search("HS 60").results
    assert len(items) >= 10


@screenshot
def test_has_no_results():
    home = pages.Homepage()
    search = home.search("asdfasdf")
    assert search.no_results


