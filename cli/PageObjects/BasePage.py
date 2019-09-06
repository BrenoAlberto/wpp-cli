from selenium import webdriver
from cli.utils import get_path_from_root_dir, set_conf


class BasePage:

    def __init__(self, save_session: bool):
        self.browserProfile = webdriver.ChromeOptions()
        chrome_driver = get_path_from_root_dir('bin/chromedriver.exe')

        if save_session:
            set_conf('saved_session', "True")
            user_data_dir = get_path_from_root_dir('data/User_Data')
            self.browserProfile.add_argument(f"--user-data-dir={user_data_dir}")

        self.browser = webdriver.Chrome(chrome_driver, chrome_options=self.browserProfile)
        self.browser.get('https://web.whatsapp.com/')

    def exit_browser(self):
        self.browser.quit()
