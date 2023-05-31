
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import json


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

        for quest in quest_list:
            print(f'start quest: {quest}')
            driver.get(quest)
            try:
                for xpath in quest_list[quest]:
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
                    time.sleep(random.randint(1, 5))
            except Exception as ex:
                print('!!! error or probably completed')
            print(f'finish quest: {quest}:')

        driver.quit()
        requests.get(close_url)
    except Exception as ex:
        print(f'ERROR {ex}')
        driver.quit()
        requests.get(close_url)


def close_other_handles(driver):
    curr = driver.current_window_handle
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if handle != curr:
            driver.close()


if __name__ == '__main__':
    # получаем из файла айдишники профилей из adspower
    with open("_ids.txt", "r") as f:
        ids = [row.strip() for row in f]

    # получаем из файла квесты
    f = open('_quests.json')
    quests = json.load(f)

    # перебираем все профили и стартуем квесты
    for index, item in enumerate(ids, start=0):
        print(f'========= {index+1}/{len(ids)} =========')
        print(f'start profile {item}')
        start_quests(item, quests)
        print(f'finish profile {item}')
        if index < len(ids):
            t = random.randint(5, 15)
            print(f'wait {t} sec')
            time.sleep(t)
        time.sleep(1)
    print('*************************')
    print(f'ALL PROFILES COMPLETED')
    print('*************************')
