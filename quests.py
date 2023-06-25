import random
import json
from datetime import datetime
from utils import *
from Drv import *


xpath_user = "//button[@type='button']//img[@alt='avatar']"
xpath_completed = "//p[normalize-space()='Completed']"

xpath_begin = "//button[normalize-space()='Begin']"
xpath_continue = "//button[normalize-space()='Continue']"
xpath_continue2 = "//button[normalize-space()='Continue']//span"
xpath_continue3 = "//a[normalize-space()='Continue']"
xpath_verify = "//button[normalize-space()='Verify']"
xpath_skip = "//button[normalize-space()='Skip']"
xpath_open = "//button[normalize-space()='Open']"

xpath_level = "//h2[normalize-space()='Level']"
xpath_score = "//p[normalize-space()='XP']"


def try_click(quest_list, quest_link):
    global begin
    try:
        # debug(f'xpath_user')
        if drv.try_xpath(xpath_user):
            if quest_link != drv.driver.current_url: # если адрес страницы изменился - значит квест закончен
                debug('>>>>>>>>>>>>> change page')
                begin = False
                return True
            
            if len(quest_list[quest_link]) > 0:  # если в квесте есть ответы
                drv.get_compare(quest_list[quest_link]) # кликаем если совпало
            
            elements = drv.get_all_elements(".//*[text()='Begin'] | .//*[text()='Skip'] | .//*[text()='Open'] | .//*[text()='Verify'] | .//*[text()='Continue']")
            elements_text = []
            for e in (elements):
                elements_text.append(e.text)
            debug(f'{elements_text} - begin: {begin}')
            timer(random.randint(2, 3))
            
            if 'Begin' in elements_text and not begin:
                if drv.try_xpath(xpath_begin, True):
                    begin = True
                    debug('Begin')
                    try_click(quest_list, quest_link)
                else: debug('Begin not clicked')
            elif 'Open' in elements_text:
                if drv.try_xpath(xpath_open, True):
                    debug('Open')
                    try_click(quest_list, quest_link)
                else: debug('Open not clicked')
            elif 'Skip' in elements_text:
                if drv.try_xpath(xpath_skip, True):
                    debug('Skip')
                    try_click(quest_list, quest_link)
                else: debug('Skip not clicked')
            elif 'Verify' in elements_text:
                if drv.try_xpath(xpath_verify, True):
                    debug('Verify')
                    try_click(quest_list, quest_link)
                else: debug('Verify not clicked')
            elif 'Continue' in elements_text:
                if drv.try_xpath(xpath_continue, True):
                    debug('Continue')
                    try_click(quest_list, quest_link)
                elif drv.try_xpath(xpath_continue2, True):
                    debug('Continue2')
                    try_click(quest_list, quest_link)
                else: debug('Continue not clicked')
                
            return True
            
    except Exception as ex:
        debug(ex)
        return False


def start_quests(quest_list):
    for i, quest_link in enumerate(quest_list, start=0):
        log(f'---- quest {i + 1} of {len(quest_list)} ----')
        log(f'start quest: {quest_link}')
        drv.close_other_handles()
        drv.driver.get(quest_link)
        if drv.try_xpath(xpath_completed, 30):
            log('! quest already completed')
            timer(random.randint(1, 3))
        else:
            # i = 0
            # while not try_click(quest_list, quest_link):
            #     reload_page(quest_list)
            #     i += 1
            #     if i > 3:
            #         break
            # log(f'finish quest: {quest_link}')
            if try_click(quest_list, quest_link):                
                log(f'finish quest: {quest_link}')
            else:
                log(f'reload page')
                drv.driver.refresh()
                try_click(quest_list, quest_link)



def get_level():
    drv.driver.get('https://layer3.xyz/quests')
    level = drv.try_xpath(xpath_level, False, 30, True)
    score = drv.try_xpath(xpath_score, False, 30, True)
    log('---------------')
    log(f'finish profile {level.text} ({score.text})')

def debug(txt):
    if debug_on:
        log(f'{txt}                           ')

if __name__ == '__main__':
    # получаем из файла айдишники профилей из adspower
    with open("_ids.txt", "r") as f:
        ids = [row.strip() for row in f]

    # получаем из файла квесты
    with open("_quests.json", "r") as f:
        quests = json.load(f)

    log(datetime.now())
    drv = Drv()
    debug_on = True
    begin = False

    # перебираем все профили и стартуем квесты
    for index, ads_id in enumerate(ids, start=0):
        log(f'========= PROFILE: {index + 1} of {len(ids)} =========')
        log(f'start profile {ads_id}')

        if drv.driver_init(ads_id):
            start_quests(quests)
            get_level()

            drv.driver.quit()
            requests.get(f'{drv.close_url}{ads_id}')
        else:
            log(f'! error init driver for {ads_id}')

        if index < len(ids):
            t = random.randint(5, 15)
            log(f'wait {t} sec')
            time.sleep(t)
        time.sleep(1)
    log('*************************')
    log(f'ALL PROFILES COMPLETED')
    log('*************************')
