import cli.PageObjects.utils as utils
from selenium.webdriver.common.by import By


class QrCodePage:
    __QR_CODE = (By.XPATH, '//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div')

    def __init__(self, browser):
        self.browser = browser
        utils.wait_element_to_be_visible(self.browser, *self.__QR_CODE)
