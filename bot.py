import base64
import logging
import random
from time import sleep

import selenium
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import secrets

# for handler in logging.root.handlers[:]:
#     logging.root.removeHandler(handler)
logging.root.handlers = list()
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(module)s:%(lineno)d - %(message)s",
                    filename="tinderBot.log",
                    filemode="w"
                    )

timeout_global = 20


class TinderBot:
    def __init__(self):
        self.driver = self.create_webdriver()
        self.login()
        self.ready_to_swipe()
        self.auto_swipe()

    @staticmethod
    def create_webdriver():
        try:
            driver = webdriver.Chrome()
        except Exception as excp:
            logging.exception("Unable to create Chrome Instance, Nested Exception is- %s", excp)
            return None
        logging.info("Successfully Created Webdriver Instance")
        return driver

    def login(self):
        self.driver.get("https://tinder.com")
        login_button = None
        try:
            logging.info("Trying find Login Button")
            login_button = WebDriverWait(driver=self.driver, timeout=timeout_global).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-manager"]/div/div/div/div'
                                                      '/div[3]/span/div[2]/button'))
            )
        except selenium.common.exceptions.NoSuchElementException as NSEexcp:
            logging.exception("Unable to Locate Login Button, Will retry with different Button",
                              NSEexcp)
        except selenium.common.exceptions.TimeoutException as ToutExcp:
            logging.exception("First Element Timed out, Will Retry with different Button", ToutExcp)
        except Exception as excp:
            logging.exception("Exception while getting login Button, Nested Exception is- %s", excp)
            return
        if not login_button:
            try:
                logging.info("retrying with different URL")
                login_button = WebDriverWait(driver=self.driver, timeout=timeout_global).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-manager"]/div/div/div'
                                                          '/div/div[3]/span/div[2]/button'))
                )
            except selenium.common.exceptions.NoSuchElementException as NSEexcp:
                logging.info("Unable to Locate Login Button on Second attempt, Aborting",
                             NSEexcp)
                return
            except selenium.common.exceptions.TimeoutException as ToutExcp:
                logging.exception("Second Element Timed out, Aborting",
                                  ToutExcp)
                return
            except Exception as excp:
                logging.exception("Exception while getting login Button, Nested Exception is- %s",
                                  excp)
                return
        self.randwait()
        login_button.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        try:
            input_username = WebDriverWait(driver=self.driver, timeout=timeout_global).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]'))
            )
            self.send_input(input_text=secrets.username, field=input_username)
            # input_username.send_keys(secrets.username)
            password_field = WebDriverWait(driver=self.driver, timeout=timeout_global).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pass"]'))
            )
            passw = base64.standard_b64decode(secrets.password.encode('ascii'))
            self.send_input(input_text=passw.decode('ascii'), field=password_field)
            # password_field.send_keys(passw.decode('ascii'))
        except Exception as excp:
            logging.exception("Exception while waiting for login button")
            return
        fb_login = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        self.randwait()
        fb_login.click()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def ready_to_swipe(self):
        try:
            logging.info("Trying to locate Location Allow Button")
            location = WebDriverWait(driver=self.driver, timeout=timeout_global).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'))
            )
        except selenium.common.exceptions.TimeoutException as ToutExcp:
            logging.exception("Unable to find Allow Location Button, Holding Execution")
        logging.info("Successfully Located Allow Location Button")
        location.click()
        self.randwait()
        try:
            logging.info("Trying to locate notification Disallow Button")
            notif = self.driver.find_element_by_xpath(
                '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        except Exception as excp:
            logging.exception("Unable to find locate notification button, Holding Execution")
        logging.info("Successfully Located notification button")
        notif.click()

    def like(self):
        like_button = WebDriverWait(driver=self.driver, timeout=60).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div['
                                                  '1]/div/div/div[1]/div/div[2]/div[4]/button'))
        )
        self.randwait()
        like_button.click()

    def dislike(self):
        dislike_button = WebDriverWait(driver=self.driver, timeout=60).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="content"]/div/div[1]/div/main/div['
                                        '1]/div/div/div[1]/div/div[2]/div[2]/button'))
        )
        self.randwait()
        dislike_button.click()

    def randwait(self):
        wait_time = random.uniform(4.9999999, 10.00000001)
        logging.info("Sleep Commencing for %s seconds", str(wait_time))
        sleep(wait_time)
        logging.info("Nap Complete")
        # self.driver.implicitly_wait(wait_time)

    def tinder_plus_popup_go_away(self):
        try:
            away_button = WebDriverWait(driver=self.driver, timeout=30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="modal-manager"]/div/div/div[3]/button[2]'))
            )
        except Exception as excp:
            return
        away_button.click()
        logging.info('Tinder Plus Popup Shooed Away')

    def send_input(self, input_text, field):
        for c in input_text:
            typeSpeed = random.uniform(0.2, 0.4000000001)
            logging.info("Sleep Commence for %s seconds", str(typeSpeed))
            sleep(typeSpeed)
            logging.info("Nap Complete")
            # self.driver.implicitly_wait(typeSpeed)
            field.send_keys(c)

    def auto_swipe(self):
        skipper_prob = 0.90
        while True:
            current_var = random.random()
            if current_var < skipper_prob:
                self.like()
            else:
                self.dislike()
            self.randwait()
            self.tinder_plus_popup_go_away()

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    bot = TinderBot()
    del bot
