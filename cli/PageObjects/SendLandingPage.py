import cli.PageObjects.utils as utils
from selenium.webdriver.common.by import By


class SendLandingPage:
    __SEND_MESSAGE_BUTTON = (By.ID, 'action-button')

    def click_send_message_button(self, browser):
        utils.wait_element_to_be_visible(browser, *self.__SEND_MESSAGE_BUTTON)
        send_message_button = utils.return_web_element(browser, *self.__SEND_MESSAGE_BUTTON)
        send_message_button.click()
