from ui.locators.base_locators import BasePageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    locators = BasePageLocators

    def select_card_value(self, value):
        self.scroll_to(self.locators.SECTION_CARD_TITLES)
        self.click(self.locators.CARD_BUTTON(self, value))
