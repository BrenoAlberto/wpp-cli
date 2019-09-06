from cli.PageObjects.BasePage import BasePage
from cli.PageObjects.SendLandingPage import SendLandingPage
from cli.PageObjects.QrCodePage import QrCodePage
from cli.PageObjects.WebAppPage import WebAppPage
from cli.utils import log, get_conf
from typing import List

# Confirm message sendend
# //span[@class="_3fnHB"][contains(.,'19:31')]

class MessageSender:
    def __init__(self, save_session):
        self.browser = self.__enter_base_page(save_session)

    def exit_browser(self) -> None:
        self.browser.quit()

    def send_msgs(self, numbers: List[int], message: str, send_image_before_msg: bool = False,
                  img_path: str = '') -> None:

        self.__wait_until_qr_code_is_validated()

        for number in numbers:
            log(f'sending message to {number}')
            self.__load_send_landing_page(number)

            send_landing_page = SendLandingPage()
            send_landing_page.click_send_message_button(self.browser)

            web_app_page = WebAppPage(self.browser)
            web_app_page.check_if_num_exists()

            if img_path != '':
                if send_image_before_msg:
                    web_app_page.send_img(img_path)
                    web_app_page.send_message(message)
                else:
                    web_app_page.send_message(message)
                    web_app_page.send_img(img_path)
            else:
                web_app_page.send_message(message)

    @staticmethod
    def __enter_base_page(save_session):
        base_page = BasePage(save_session)
        return base_page.browser

    def __wait_until_qr_code_is_validated(self):
        if not get_conf('saved_session'):
            QrCodePage(self.browser)

        WebAppPage(self.browser)

    def __load_send_landing_page(self, number):
        self.browser.get(f'https://api.whatsapp.com/send?phone=55{number}')
