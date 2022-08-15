from selenium.webdriver.common.by import By

class BasePageLocators(object):
    SECTION_CARD_TITLES = (By.XPATH, '//h3[contains(text(), "Номинал карты")]')
    CARD_BUTTON = lambda self, value: (By.XPATH, f'//li[contains(@data-value, "{value}")]')
    CARD_INPUT = (By.XPATH, '//input[contains(@name, "nominal_value")]')
    CARD_BUTTON_ACTIVE = (By.CSS_SELECTOR, 'button.par-options__button--active')