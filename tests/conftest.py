import os
import pytest
from appium import webdriver
from page_object.pages import MainShowsPage


PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

app_params = {}
app_params['platformName'] = 'Android'
app_params['platformVersion'] = '5.1'
app_params['deviceName'] = 'Android Emulator'
app_params['app'] = \
    PATH('/Users/kapusha/Desktop/thailand/SeriesGuide/SeriesGuide/build/outputs/apk/SeriesGuide-free-debug.apk')


@pytest.yield_fixture(scope='function')
def main_shows_page():
    driver = webdriver.Remote('http://localhost:4723/wd/hub', app_params)
    # driver.implicitly_wait(15)
    yield MainShowsPage(driver)
    driver.quit()
