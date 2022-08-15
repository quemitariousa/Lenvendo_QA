import allure
import pytest

import files.userdata
from ui.tests_UI.base import BaseCase


class TestMainPage(BaseCase):
    @allure.epic('UI tests')
    @allure.feature('Card')
    @allure.title('Test select card')
    @pytest.mark.parametrize('value', ["500", "1000", "2000", "3000", "5000", "10000"])
    def test_card_values(self, value, main_page):
        self.base_page.auth(files.userdata.login_test, files.userdata.pw_test)
        main_page.select_card_value(value)
        assert main_page.wait_find(main_page.locators.CARD_BUTTON_ACTIVE).text == value
        assert main_page.wait_find(main_page.locators.CARD_INPUT).get_attribute("value") == value
