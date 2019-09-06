import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from typing import List
from .utils import log, get_path_from_root_dir


class MessageSender:

    def __init__(self, save_session: bool) -> None:
        self.browserProfile = webdriver.ChromeOptions()

        if save_session:
            user_data_dir = get_path_from_root_dir('data/User_Data')
            chrome_driver = get_path_from_root_dir('bin/chromedriver.exe')
            self.browserProfile.add_argument(f"--user-data-dir={user_data_dir}")

        self.browser = webdriver.Chrome(chrome_driver, chrome_options=self.browserProfile)

    class NumberDoesNotExists(Exception):
        pass

    def exit_browser(self) -> None:
        self.browser.quit()

    def send_msgs(self, numbers: List[int], message: str, send_image_before_msg: bool = False,
                  img_path: str = '') -> None:
        for number in numbers:
            log(f'sending message to {number}')
            self.__load_page_and_send_msg(number, message, img_path, send_image_before_msg)

    def __load_page(self, url: str) -> None:
        self.browser.get(url)
        time.sleep(2)
        self.__wait_element_load_then_click("//*[@id='action-button']")

    def __wait_until_page_loads(self) -> bool:
        time.sleep(2)

        scan_qrcode = self.browser.find_elements_by_xpath("//*[@id='app']/div/div/div[2]/div[1]/div/div[2]/div[2]/img")
        keep_connected = self.browser.find_elements_by_xpath("//*[@id='app']/div/div/div[4]/div/div/div[2]/h1")
        num_does_not_exists = self.browser.find_elements_by_xpath("//*[contains(text(), 'inválido')]")
        startup_loading = self.browser.find_elements_by_xpath('//*[@id="startup"]/div')
        initializing = self.browser.find_elements_by_xpath("//*[contains(text(), 'Iniciando')]")

        if len(num_does_not_exists) > 0 and num_does_not_exists[0].is_displayed():
            raise self.NumberDoesNotExists

        try:
            if len(scan_qrcode) > 0 and scan_qrcode[0].is_displayed():
                self.__wait_until_page_loads()

            elif len(keep_connected) > 0 and keep_connected[0].is_displayed():
                self.__wait_until_page_loads()

            elif len(startup_loading) > 0 and startup_loading[0].is_displayed():
                self.__wait_until_page_loads()

            elif len(initializing) > 0 and initializing[0].is_displayed():
                self.__wait_until_page_loads()
        except StaleElementReferenceException:
            self.__wait_until_page_loads()

        return True

    def __send_img(self, img_path: str) -> None:
        self.__wait_element_load_then_click("//*[@id='main']/header/div[3]/div/div[2]/div/span")
        self.__wait_element_load_then_send_keys(
            "//*[@id='main']/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input", img_path)
        self.__wait_element_load_then_click(
            "//*[@id='app']/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div")
        time.sleep(2)

    def __send_msg(self, message: str) -> None:
        self.__wait_element_load_then_send_keys("//*[@id='main']/footer/div[1]/div[2]/div/div[2]", message)
        self.__wait_element_load_then_click("//*[@id='main']/footer/div[1]/div[3]/button")

    def __load_page_and_send_msg(self, number: int, message: str, img_path: str, send_image_before_msg: bool) -> None:
        try:
            self.__load_page(f'https://api.whatsapp.com/send?phone=55{number}')
            self.__wait_until_page_loads()
            if img_path != '':
                if send_image_before_msg:
                    self.__send_img(img_path)
                    self.__send_msg(message)
                else:
                    self.__send_msg(message)
                    self.__send_img(img_path)
            else:
                self.__send_msg(message)
        except self.NumberDoesNotExists:
            log(f'the number {number} does not exists')

    def __wait_element_load_then_send_keys(self, xpath: str, keys: str) -> None:
        element = self.browser.find_elements_by_xpath(xpath)
        print(f'wait el load send key {keys}')
        if len(element) > 0 and element[0].is_displayed():
            element[0].send_keys(keys)
            time.sleep(2)
        else:
            self.__wait_element_load_then_send_keys(xpath, keys)

    def __wait_element_load_then_click(self, xpath: str) -> None:
        element = self.browser.find_elements_by_xpath(xpath)

        if len(element) > 0 and element[0].is_displayed():
            element[0].click()
            time.sleep(2)
        else:
            self.__wait_element_load_then_click(xpath)
