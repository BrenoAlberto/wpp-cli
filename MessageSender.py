from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from typing import List
import time

class MessageSender():
    def __init__(self, numbers: List[int], message: str, img_path: str, send_img_before: bool, save_session: bool):
        if save_session == True:
            self.browserProfile = webdriver.ChromeOptions()
            self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            self.browserProfile.add_argument('--user-data-dir=./User_Data')
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.numbers = numbers
        self.message = message
        self.img_path = img_path
        self.send_img_before = send_img_before

    def send_msgs(self, numbers: List[int], message: str):
        for number in numbers:
            self.__load_page_and_send_msg(number, message)

    def __load_page(self, url: str):
        self.browser.get(url)
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='action-button']").click()

    def __check_loaded_page(self):
        time.sleep(2)
        keep_connected = self.browser.find_elements_by_xpath("//*[@id='app']/div/div/div[4]/div/div/div[2]/h1")
        num_does_not_exists = self.browser.find_elements_by_xpath("//*[contains(text(), 'inválido')]")
        startup_loading = self.browser.find_elements_by_xpath('//*[@id="startup"]/div')
        initializing = self.browser.find_elements_by_xpath("//*[contains(text(), 'Iniciando')]")

        if len(num_does_not_exists) > 0 and num_does_not_exists[0].is_displayed():
            print('The number does not exists')
            return
        
        if len(keep_connected) > 0 and keep_connected[0].is_displayed():
            self.__check_loaded_page()
        
        elif len(startup_loading) > 0 and startup_loading[0].is_displayed():
            self.__check_loaded_page()

        elif len(initializing) > 0 and initializing[0].is_displayed():
            self.__check_loaded_page()

    def __send_msg(self, message: str):
        message_input = self.browser.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
        message_input.send_keys(message)
        self.browser.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()

    def __load_page_and_send_msg(self, number: int, message: str):
        self.__load_page("https://api.whatsapp.com/send?phone=55" + str(number))
        self.__check_loaded_page()
        self.__send_msg(message)