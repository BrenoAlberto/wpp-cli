import cli.PageObjects.utils as utils
from selenium.webdriver.common.by import By


class WebAppPage:
    __PROFILE_HEADER = (By.XPATH, '//*[@id="side"]/header')
    __CLIP_ICON = (By.XPATH, '//*[@id="main"]/header/div[3]/div/div[2]/div')
    __IMAGE_INPUT = (By.XPATH, '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input')
    __DOCUMENT_INPUT = (By.XPATH, '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button/input')
    __MESSAGE_INPUT = (By.CLASS_NAME, '_1PRhq')
    __SEND_MESSAGE_BUTTON = (By.XPATH, '//*[@id="main"]/footer/div[1]/div[3]/button')
    __SEND_FILE_BUTTON = (By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div')
    __NUM_DOES_NOT_EXISTS_ALERT = (By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div')

    def __init__(self, browser):
        self.browser = browser
        utils.wait_element_to_be_visible(self.browser, *self.__PROFILE_HEADER)

    def check_if_num_exists(self):
        if utils.element_does_exists(self.browser, *self.__NUM_DOES_NOT_EXISTS_ALERT):
            return False
        return True

    def send_message(self, message):
        self._write_message(message)
        self._click_send_message()

    def send_img(self, img_path):
        self._click_clip_icon()
        self._input_img(img_path)
        self._click_send_file()

    def send_document(self, document_path):
        self._click_clip_icon()
        self._input_document(document_path)
        self._click_send_file()

    def _input_img(self, img_path):
        image_input = utils.return_web_element(self.browser, *self.__IMAGE_INPUT)
        image_input.send_keys(img_path)

    def _input_document(self, document_path):
        document_input = utils.return_web_element(self.browser, *self.__DOCUMENT_INPUT)
        document_input.send_keys(document_path)

    def _write_message(self, message):
        message_input = utils.return_web_element(self.browser, *self.__MESSAGE_INPUT)
        message_input.send_keys(message)

    def _click_send_message(self):
        send_message_button = utils.return_web_element(self.browser, *self.__SEND_MESSAGE_BUTTON)
        send_message_button.click()

    def _click_send_file(self):
        utils.wait_element_to_be_visible(self.browser, *self.__SEND_FILE_BUTTON)
        send_file_button = utils.return_web_element(self.browser, *self.__SEND_FILE_BUTTON)
        send_file_button.click()

    def _click_clip_icon(self):
        clip_icon = utils.return_web_element(self.browser, *self.__CLIP_ICON)
        clip_icon.click()
