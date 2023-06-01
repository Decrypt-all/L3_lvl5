import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import json
from datetime import datetime


def start_quests(ads_id, quest_list):
    open_url = f'http://local.adspower.net:50325/api/v1/browser/start?user_id={ads_id}'
    close_url = f'http://local.adspower.net:50325/api/v1/browser/stop?user_id={ads_id}'
    driver = None
    try:
        resp = requests.get(open_url).json()

        chrome_driver = resp["data"]["webdriver"]
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)

        close_other_handles(driver)

        for i, quest in enumerate(quest_list, start=0):
            log(f'---- quest {i + 1} of {len(quest_list)} ----')
            log(f'start quest: {quest}')
            driver.get(quest)
            try:
                xpath_completed = '/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/p[1]'
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_completed)))
                log('! quest already completed')
                time.sleep(random.randint(1, 3))
            except Exception as ex:
                try:
                    for xpath in quest_list[quest]:
                        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
                        time.sleep(random.randint(1, 5))
                except Exception as ex:
                    log('>>>>>>>> !!! error')
                log(f'finish quest: {quest}')

        get_level(driver)
        driver.quit()
        requests.get(close_url)
    except Exception as ex:
        log(f'>>>>>>>> !!! ERROR {ex}')
        driver.quit()
        requests.get(close_url)


def get_level(driver):
    driver.get('https://layer3.xyz/quests')
    xpath1 = '/html[1]/body[1]/div[1]/div[1]/div[3]/div[2]/div[2]/div[3]/div[1]/div[1]/h2[1]'
    xpath2 = '/html[1]/body[1]/div[1]/div[1]/div[3]/div[2]/div[2]/div[3]/div[1]/div[1]/p[1]'
    res1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath1)))
    res2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath2)))
    log('---------------')
    log(f'finish profile {item} | {res1.text} ({res2.text})')


def close_other_handles(driver):
    curr = driver.current_window_handle
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if handle != curr:
            driver.close()


def log(txt):
    print(txt)
    file = open("log.txt", "a")  # append mode
    file.write(f"{txt} \n")
    file.close()


if __name__ == '__main__':
    # получаем из файла айдишники профилей из adspower
    with open("_ids.txt", "r") as f:
        ids = [row.strip() for row in f]

    # получаем из файла квесты
    f = open('_quests.json')
    quests = json.load(f)

    log(datetime.now())

    # перебираем все профили и стартуем квесты
    for index, item in enumerate(ids, start=0):
        log(f'========= PROFILE: {index + 1} of {len(ids)} =========')
        log(f'start profile {item}')
        start_quests(item, quests)

        if index < len(ids):
            t = random.randint(5, 15)
            log(f'wait {t} sec')
            time.sleep(t)
        time.sleep(1)
    log('*************************')
    log(f'ALL PROFILES COMPLETED')
    log('*************************')
