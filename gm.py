
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import random
from selenium.webdriver.chrome.service import Service


xpath_check = "//h2[normalize-space()='Проверка безопасности подключения к сайту']"
xpath_user = "//button[@type='button']//img[@alt='avatar']"
xpath_gm = "//div[@class='flex flex-col gap-lg pr-md mt-3xl']//span[@class='c-kXzUB c-kXzUB-icCitdK-css']"
xpath_gm_mini = "//div[@class='c-PJLV c-PJLV-illovkd-css']//span[@class='c-kXzUB c-kXzUB-icCitdK-css']"
xpath_streak = "//p[@class='c-iKqlBJ c-iKqlBJ-hgrifu-size-xxs c-iKqlBJ-cmVlgk-align-left c-iKqlBJ-fVyUfA-color-secondary c-iKqlBJ-iqKmYR-fontWeight-medium']"
xpath_open = "//button[normalize-space()='Open']"

open_url = 'http://local.adspower.net:50325/api/v1/browser/start?user_id='
close_url = 'http://local.adspower.net:50325/api/v1/browser/stop?user_id='
driver: WebDriver
debug_on = False


def driver_init(ads_id):
    global driver
    try:
        resp = requests.get(f'{open_url}{ads_id}').json()
        chrome_driver = resp["data"]["webdriver"]
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(service=Service(chrome_driver), options=chrome_options)
        return True
    except Exception as ex:
        log(f'ERROR {ex}')
        return False


def problem_start(ads_id):
    if try_xpath(xpath_check):
        driver.refresh()
        driver.quit()
        timer(15)

        driver_init(ads_id)
        try_xpath('//*[@id="challenge-stage"]/div/label/input')
        driver.quit()
        timer(10)

        start_gm(ads_id, False)
        return True
    else:
        return False


def start_gm(ads_id, first_start):
    debug(f'start_gm first_start: {first_start}')
    global driver
    if driver_init(ads_id):
        if first_start:
            close_other_handles()
            driver.get('https://layer3.xyz/quests')

        if not problem_start(ads_id):
            try_gm()
        debug('start_gm 0001')
        driver.quit()
        debug('start_gm 0002 driver.quit')
        requests.get(f'{close_url}{ads_id}')
        debug('start_gm 0003 requests.get')
    else:
        debug('start_gm 0004 driver_init FALSE')
        driver.quit()
        requests.get(f'{close_url}{ads_id}')


def try_xpath(xpath, click=False, sec=3):
    try:
        if click:
            debug('try_xpath click')
            WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, xpath))).click()
        else:
            debug(f'try_xpath: {xpath}')
            WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, xpath)))
        return True
    except Exception as ex:
        return False


def try_gm():
    if try_xpath(xpath_user, False, 30):
        if try_xpath(xpath_streak):
            log(f'~ already completed')
        else:
            if try_xpath(xpath_gm, True) or try_xpath(xpath_gm_mini, True):
                if try_xpath(xpath_open, True, 5):
                    log(f'+ gm completed (box)')
                    time.sleep(3)
                elif try_xpath(xpath_streak):
                    log(f'+ gm completed')
                else:
                    reload_page()
            else:
                reload_page()
    else:
        reload_page()


def reload_page():
    log(f'reload page')
    driver.refresh()
    try_gm()


def close_other_handles():
    curr = driver.current_window_handle
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if handle != curr:
            driver.close()


def log(txt):
    print(txt)
    file = open("log_gm.txt", "a")  # append mode
    file.write(f"{txt} \n")
    file.close()


def debug(txt):
    if debug_on:
        log(txt)



def timer(sec):
    if sec >= 0:
        print(f'wait: {sec} sec.   ', end='')
        time.sleep(1)
        print('\r', end='')
        sec -= 1
        timer(sec)


if __name__ == '__main__':
    with open("_ids.txt", "r") as f:
        ids = [row.strip() for row in f]

    log(datetime.now())

    for index, item in enumerate(ids, start=0):
        log(f'========= {index+1}/{len(ids)} =========')
        log(f'start profile {item}')

        start_gm(item, True)

        log(f'finish profile {item}')
        if (index+1) < len(ids):
            t = random.randint(5, 15)
            timer(t)
        time.sleep(1)
    log('*************************')
    log(f'ALL PROFILES COMPLETED')
    log('*************************')
    log(datetime.now())