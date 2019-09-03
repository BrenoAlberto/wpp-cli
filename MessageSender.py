from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from typing import List
import time

class MessageSender():
    def __init__(self, save_session: bool) -> None:
        self.browserProfile = None

        if save_session == True:
            self.browserProfile = webdriver.ChromeOptions()
            self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            self.browserProfile.add_argument('--user-data-dir=./User_Data')

        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)

    def send_msgs(self, numbers: List[int], message: str, send_image_before_msg: bool = False, image_path: str = '') -> None:
        for number in numbers:
            print(number)
            self.__load_page_and_send_msg(number, message, image_path, send_image_before_msg)

    def __load_page(self, url: str) -> None:
        self.browser.get(url)
        time.sleep(2)
        self.__wait_element_load_then_click("//*[@id='action-button']")

    def __check_loaded_page(self) -> None:
        time.sleep(2)

        scan_qrcode = self.browser.find_elements_by_xpath("//*[@id='app']/div/div/div[2]/div[1]/div/div[2]/div[2]/img")
        keep_connected = self.browser.find_elements_by_xpath("//*[@id='app']/div/div/div[4]/div/div/div[2]/h1")
        num_does_not_exists = self.browser.find_elements_by_xpath("//*[contains(text(), 'inválido')]")
        startup_loading = self.browser.find_elements_by_xpath('//*[@id="startup"]/div')
        initializing = self.browser.find_elements_by_xpath("//*[contains(text(), 'Iniciando')]")

        try:
            if len(num_does_not_exists) > 0 and num_does_not_exists[0].is_displayed():
                print('The number does not exists')
                return

            if len(scan_qrcode) > 0 and scan_qrcode[0].is_displayed():
                self.__check_loaded_page()
            
            elif len(keep_connected) > 0 and keep_connected[0].is_displayed():
                self.__check_loaded_page()
            
            elif len(startup_loading) > 0 and startup_loading[0].is_displayed():
                self.__check_loaded_page()

            elif len(initializing) > 0 and initializing[0].is_displayed():
                self.__check_loaded_page()
        except StaleElementReferenceException:
            self.__check_loaded_page()

    def __send_img(self, img_path: str) -> None:
        self.__wait_element_load_then_click("//*[@id='main']/header/div[3]/div/div[2]/div/span")
        self.__wait_element_load_then_send_keys("//*[@id='main']/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input", img_path)
        self.__wait_element_load_then_click("//*[@id='app']/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div")
        time.sleep(2)

    def __send_msg(self, message: str) -> None:
        self.__wait_element_load_then_send_keys("//*[@id='main']/footer/div[1]/div[2]/div/div[2]", message)
        self.__wait_element_load_then_click("//*[@id='main']/footer/div[1]/div[3]/button")

    def __load_page_and_send_msg(self, number: int, message: str, image_path: str, send_image_before_msg: bool) -> None:
        self.__load_page("https://api.whatsapp.com/send?phone=55" + str(number))
        self.__check_loaded_page()

        if image_path != '':
            if send_image_before_msg == True:
                self.__send_img(image_path)
                self.__send_msg(message)
            else:
                self.__send_msg(message)
                self.__send_img(image_path)
        else:
            self.__send_msg(message)

    def __wait_element_load_then_send_keys(self, xpath: str, keys: str) -> None:
        element = self.browser.find_elements_by_xpath(xpath)

        if len(element) > 0 and element[0].is_displayed():
            element[0].send_keys(keys)
            time.sleep(2)
        else :
            self.__wait_element_load_then_send_keys(xpath, keys)

    def __wait_element_load_then_click(self, xpath: str) -> None:
        element = self.browser.find_elements_by_xpath(xpath)

        if len(element) > 0 and element[0].is_displayed():
            element[0].click()
            time.sleep(2)
        else:
            self.__wait_element_load_then_click(xpath)
        