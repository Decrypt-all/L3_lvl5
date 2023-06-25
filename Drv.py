from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import requests
from utils import *


class Drv:
    def __init__(self) -> bool:
        self.open_url = 'http://local.adspower.net:50325/api/v1/browser/start?user_id='
        self.close_url = 'http://local.adspower.net:50325/api/v1/browser/stop?user_id='


    def driver_init(self, ads_id):
        try:
            resp = requests.get(f'{self.open_url}{ads_id}').json()
            chrome_driver = resp["data"]["webdriver"]
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
            self.driver = webdriver.Chrome(service=Service(chrome_driver), options=chrome_options)
            return True
        except Exception as ex:
            log(f'ERROR {ex}')
            return False
        
    def get_all_elements(self, xpath)->list[WebElement]:
        return WebDriverWait(self.driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

        
    def get_compare(self, quests):
        try:
            buttons = self.get_all_elements("//button")
            buttons_text = {}
            for b in buttons:
                buttons_text[b.text] = b
            for key in buttons_text:
                for q in quests:
                    if q in key:
                        buttons_text[key].click()
                        return True
        except Exception as ex:
            return False

    def try_xpath(self, xpath, click=False, sec=3, ret_obj=False):
        try:
            if click:
                WebDriverWait(self.driver, sec).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
            elif ret_obj:
                return WebDriverWait(self.driver, sec).until(EC.presence_of_element_located((By.XPATH, xpath)))
            else:
                WebDriverWait(self.driver, sec).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception as ex:
            #log(ex)
            return False

    def close_other_handles(self):
        curr = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if handle != curr:
                self.driver.close()


