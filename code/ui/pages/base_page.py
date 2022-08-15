import time
import allure

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

class PageNotOpenedException(Exception):
    pass


CLICK_RETRY = 5


class BasePage(object):
    url = 'http://qa.digift.ru/'

    def __init__(self, driver):
        self.driver = driver

    def is_opened(self, timeout=15):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url == self.url:
                return True
        raise PageNotOpenedException(f'{self.url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Looking for an element...')
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Click on an element...')
    def click(self, locator, timeout=5) -> WebElement:
        self.find(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()

    @allure.step('Sending value...')
    def send_value(self, locator, value):
        input_element = self.wait_find(locator)
        input_element.clear()
        input_element.send_keys(value)

    def wait_find(self, locator):
        WebDriverWait(self.driver, timeout=5).until(
            lambda d: self.find(locator))
        return self.find(locator)

    def scroll_to(self, locator):
        elem = self.wait_find(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(elem)

    @allure.step("Log in...")
    def auth(self, login, pw):
        self.driver.get(f"http://{login}:{pw}@qa.digift.ru")
        return self.driver

