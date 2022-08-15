import os
import shutil
import sys
import pytest
from selenium import webdriver

from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver=driver)
