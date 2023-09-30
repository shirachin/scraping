from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import requests

from dotenv import load_dotenv

import traceback
import sys
import os
import re
import pprint
import pyperclip
import asyncio

from settings.settings import CHROME_PATH, REWARD_FILTER, API_URL
from settings.search_setting import search_terms
from tool.gcvision import detect_text_uri
from tool.api import Property_api


class MyException(Exception):
    def __init__(self, *args):
        if len(args) == 0:
            args = ""
        self.arg = args


class FIND_ELEMENT_EXCEPTION(MyException):
    def __str__(self) -> str:
        return f"element_find = None <{self.args[0]}>"

load_dotenv()

login_data = [
    (os.environ['LOGIN_DATA14'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA15'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA16'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA17'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA18'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA19'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA20'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA21'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA22'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA23'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA24'], os.environ['LOGIN_DATAPW']),
    (os.environ['LOGIN_DATA25'], os.environ['LOGIN_DATAPW']),
]

RE_M = re.compile(r'[\d.]+ヶ月')
RE_P = re.compile(r'[\d.]+％')
RE_Y = re.compile(r'[\d.]+万円')

class A_driver:
    def __init__(self, test_mode: bool) -> None:
        options = Options()

        if not test_mode:
            options.add_argument("--disable-gpu")
            options.add_argument("--headless=new")

        options.add_argument("--disable-extensions")
        options.add_argument('--proxy-server="direct://"')
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.binary_location = CHROME_PATH
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver_wait = WebDriverWait(driver=self.driver, timeout=30)

    def __del__(self) -> None:
        self.driver.quit()

    def wait(self, minute: int = 1):
        sleep(minute)
        self.driver_wait.until(EC.presence_of_all_elements_located)

    def find_element(self, by, value):
        for i in range(10):
            if self.driver.find_elements(by, value):
                return self.driver.find_element(by, value)
            self.wait(2)
        raise FIND_ELEMENT_EXCEPTION

    def login(self, id_set: int = 0) -> bool:
        # ID, PW 使い切り判定
        if not (0 <= id_set and id_set < len(login_data)):
            return False

        # ログインページアクセス
        self.driver.get("https://atbb.athome.jp/")
        self.wait()

        # ログイン
        self.find_element(By.CSS_SELECTOR, "#loginFormText").send_keys(
            login_data[id_set][0]
        )
        self.find_element(By.CSS_SELECTOR, "#passFormText").send_keys(
            login_data[id_set][1]
        )
        self.wait()
        self.find_element(By.CSS_SELECTOR, "#loginSubmit").click()
        self.wait()

        # ポップアップクローズ
        if self.driver.find_elements(By.CSS_SELECTOR, '#riyousha > div > div.info_content > div:nth-child(7) > input'):
            self.find_element(By.CSS_SELECTOR, '#riyousha > div > div.info_content > div:nth-child(7) > input').click()
            self.wait()

        # 物件検索 -> 流通物件検索
        self.find_element(
            By.CSS_SELECTOR,
            "#header > header-menu > div > nav > ul > li:nth-child(1) > a",
        ).click()
        self.find_element(
            By.CSS_SELECTOR,
            "#header > header-menu > div > nav > ul > li.is-c-show > div > form > div > div:nth-child(1)",
        ).click()
        self.wait(2)

        # 新規タブへ移動
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.wait()

        # リダイレクト終了まで待機
        while "members" in self.driver.current_url:
            sleep(0.5)

        # ログイン失敗判定
        if "LoginException" in self.driver.current_url:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/header-bar/div/div/div[2]/div/div[2]/ul/form/li/button",
            ).click()
            self.wait()
            return self.login(id_set + 1)

        return True

    def logout(self):
        self.driver.get('https://atbb.athome.co.jp/front-web/mainservlet/bfhm001s001')
        self.wait()
        self.find_element(
            By.CSS_SELECTOR, 'body > table > tbody > tr:nth-child(1) > td > table:nth-child(6) > tbody > tr > td.pad05 > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > a > div'
        ).click()

    def output_search_terms(self, mode=0):
        term = search_terms[mode]
        #物件検索遷移
        self.find_element(By.XPATH, '/html/body/table/tbody/tr[1]/td/table[3]/tbody/tr/td[1]/a').click()
        self.wait()

        #１ページ目
        for t in term[0]:
            self.find_element(By.XPATH, t).click()
            self.wait()
        self.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[3]/form/span/div[1]/table[2]/tbody/tr[2]/td/div/table/tbody/tr/td[1]/input').click()
        self.wait()

        #２ページ目
        select = Select(self.find_element(By.CSS_SELECTOR, '#sentaku1ZenShikugun_13'))
        for t in term[1]:
            select.select_by_value(t)
        self.find_element(By.CSS_SELECTOR, 'body > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(1) > td.contents > form > div:nth-child(16) > input.btn06d.determineShozaichi').click()
        self.wait()

        #３ページ目
        for t in term[2]:
            self.find_element(By.XPATH, t).click()
        self.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[3]/form/div[1]/div[2]/input[1]').click()
        self.wait()

    def search(self):
        self.output_search_terms()

        res = requests.get(API_URL['checked_property']).json()
        checked_id = [i['id'] for i in res]

        Select(self.find_element(By.CSS_SELECTOR, '#firstPngDisplayCount')).select_by_value('100')
        self.wait()

        Select(self.find_element(By.CSS_SELECTOR, '#firstPngOrderBy')).select_by_value('08')
        self.wait()

        while True:
            for i in range(100):
                card_id = '#bukkenCard_' + str(i)

                try:
                    self.find_element(By.CSS_SELECTOR, card_id).find_element(By.XPATH, './/button[contains(@id, "shosai")]').click()
                except FIND_ELEMENT_EXCEPTION:
                    self.logout()

                self.wait()

                self.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[3]/form[2]/div[2]/div/div/p[2]/span/span[1]/button').click()
                self.wait(3)
                
                id = int(pyperclip.paste())
                if not id in checked_id:
                    r = self.find_element(By.XPATH, data_xpath('報酬')).text
                    if '■広告費：' in r or not REWARD_FILTER:

                        

                        data.validate()
                        pprint.pprint(vars(data))

                        data.post()
                        # 1件用
                        # break

                self.driver.back()
                self.wait()

            # 100件用
            break

    def data_pick(self, id) -> Property_api:
        data = Property_api()

        if data.id.set_param(id):
            del data
            self.driver.back()
            self.wait()

            print(f'ピック中 : {id}')
            reward_list = []
            if not REWARD_FILTER:
                rs = ''
            else:
                rs = r.split('■広告費：')[1]

            search_m = RE_M.search(rs)
            search_p = RE_P.search(rs)
            search_y = RE_Y.search(rs)
            price = int(float(detect_text_uri(self.driver.find_element(By.XPATH, '//img[contains(@id, "price_img")]').get_attribute('src')).replace('万円', '')) * 10000)
            if search_m is not None:
                reward_list.append({
                    'type': 'm',
                    'value': search_m.group(),
                    'rent': price,
                    'level': int(float(search_m.group().replace('ヶ月', '')) * 100)
                    })
            if search_p is not None:
                reward_list.append({
                    'type': 'p',
                    'value': search_p.group(),
                    'rent': price,
                    'level': int(search_p.group().replace('％', ''))
                    })
            if search_y is not None:
                level = int(float(search_y.group().replace('万円', '')) * 10000)
                reward_list.append({
                    'type': 'y',
                    'value': search_y.group(),
                    'rent': price,
                    'level': int(level / price * 100)
                    })
            if len(reward_list) == 0:
                reward_list.append({
                    'type': 'n',
                    'value': rs,
                    'rent': price,
                    'level': 0
                })

            data.reward.set_param(max([i['level'] for i in reward_list]))
            data.address_original.set_param(self.find_element(By.XPATH, data_xpath('所在地')).text.replace(' 地図を見る', ''))
            url = API_URL['geocode'] + data.address_original.value
            res = requests.get(url)
            if not res.status_code // 100 == 2:
                print(res.content)
            res_data = res.json()
            adda: list = res_data['results'][0]['address_components']
            adlist = [i['long_name'] for i in reversed(adda)]
            for i, v in enumerate(adlist):
                if i == 2:
                    data.prefecture.set_param(v)
                if i == 3:
                    data.address_lv1.set_param(v)
                if i == 4:
                    data.address_lv2.set_param(v)
                if i == 5:
                    data.address_lv3.set_param(v)
                if i == 6:
                    data.address_lv4.set_param(v)
                if i == 7:
                    data.address_lv5.set_param(v)
                if i == 8:
                    data.address_lv6.set_param(v)
                if i == 9:
                    data.address_lv7.set_param(v)

            floor_data = self.find_element(By.XPATH, data_xpath('階建/階')).text
            data.n_storey_building = int(re.search(r'[\d]+階建', floor_data).group().replace('階建', ''))
            data.floor = int(re.search(r'[\d]+階部分', floor_data).group().replace('階部分', ''))
            data.is_top_floor = data.n_storey_building == data.floor

            buil = self.find_element(By.XPATH, data_xpath('築年月')).text
            data.building_year = int(re.search(r'[\d]+年', buil).group().replace('年', ''))
            data.building_month = int(re.search(r'[\d]+月', buil).group().replace('月', ''))

            dep = self.find_element(By.XPATH, data_xpath('敷金')).text.replace('ヶ月', '')
            if dep.isdecimal():
                data.deposit = int(dep)
            else:
                data.deposit = 0
            kem = self.find_element(By.XPATH, data_xpath('礼金')).text.replace('ヶ月', '')
            if kem.isdecimal():
                data.key_money = int(kem)
            else:
                data.key_money = 0

            data.floor_plan = floor_plan_translate(self.find_element(By.XPATH, data_xpath('間取り')).text.strip())

            data.station1 = self.find_element(By.XPATH, data_xpath('交通')).text
            data.station2 = self.find_element(By.XPATH, data_xpath('利用駅1')).text
            data.station3 = self.find_element(By.XPATH, data_xpath('利用駅2')).text

            data.station1_time = sum([int(i.group()) for i in re.finditer(r'\d+', data.station1)]) if not sum([int(i.group()) for i in re.finditer(r'\d+', data.station1)]) == 0 else None
            data.station2_time = sum([int(i.group()) for i in re.finditer(r'\d+', data.station2)]) if not sum([int(i.group()) for i in re.finditer(r'\d+', data.station2)]) == 0 else None
            data.station3_time = sum([int(i.group()) for i in re.finditer(r'\d+', data.station3)]) if not sum([int(i.group()) for i in re.finditer(r'\d+', data.station3)]) == 0 else None

            data.area = self.find_element(By.XPATH, data_xpath('専有面積')).text
            data.area_num = float(re.search(r'\d+[\.]?\d+', data.area).group())

            data.building_name = self.find_element(By.XPATH, data_xpath('建物名・部屋番号')).text
            data.floor_plan_breakdown = self.find_element(By.XPATH, data_xpath('間取り内訳')).text
            data.balcony = self.find_element(By.XPATH, data_xpath('バルコニー')).text
            data.building_structure = self.find_element(By.XPATH, data_xpath('建物構造')).text
            data.units = self.find_element(By.XPATH, data_xpath('総戸数')).text
            data.area_price = self.find_element(By.XPATH, data_xpath('坪単価')).text
            data.parking_car = self.find_element(By.XPATH, data_xpath('駐車場', 'span', '../')).text
            data.parking_bike = self.find_element(By.XPATH, data_xpath('バイク置場')).text
            data.parking_bicycle = self.find_element(By.XPATH, data_xpath('駐輪場')).text
            data.main_glossy_surface = self.find_element(By.XPATH, data_xpath('主要採光面')).text
            data.administrator = self.find_element(By.XPATH, data_xpath('管理員の勤務形態')).text
            data.reform = self.find_element(By.XPATH, data_xpath('リフォーム履歴')).text
            data.renovation = self.find_element(By.XPATH, data_xpath('リノベーション履歴')).text
            data.hot_spring = self.find_element(By.XPATH, data_xpath('温泉')).text
            data.facility = self.find_element(By.XPATH, data_xpath('設備')).text
            data.special_remarks = self.find_element(By.XPATH, data_xpath('特記事項')).text
            data.remarks = self.find_element(By.XPATH, data_xpath('備考')).text
            data.environment = self.find_element(By.XPATH, data_xpath('周辺環境')).text
            data.rent = price
            data.management_fee = self.find_element(By.XPATH, data_xpath('管理費')).text
            data.maintenance_fee = self.find_element(By.XPATH, data_xpath('共益費')).text
            data.sundries = self.find_element(By.XPATH, data_xpath('雑費')).text
            data.mms_fee = self.find_element(By.XPATH, data_xpath('管理費等')).text
            data.drawing = self.find_element(By.XPATH, data_xpath('敷引')).text
            data.etc_fee = self.find_element(By.XPATH, data_xpath('鍵交換代等')).text
            data.guarantee = self.find_element(By.XPATH, data_xpath('保証金')).text
            data.depreciation_guarantee = self.find_element(By.XPATH, data_xpath('保証金償却')).text
            data.rental_guarantee = self.find_element(By.XPATH, data_xpath('賃貸保証')).text
            data.credit_card_payment = self.find_element(By.XPATH, data_xpath('クレジットカード決済')).text
            data.insurance_subscription = self.find_element(By.XPATH, data_xpath('保険等加入')).text
            data.lump_sum = self.find_element(By.XPATH, data_xpath('その他一時金')).text
            data.running_cost = self.find_element(By.XPATH, data_xpath('ランニングコスト')).text
            data.present_condition = self.find_element(By.XPATH, data_xpath('現況')).text
            data.matricration_date = self.find_element(By.XPATH, data_xpath('入居日')).text
            data.contract_period = self.find_element(By.XPATH, data_xpath('契約期間')).text
            data.renewal_fee = self.find_element(By.XPATH, data_xpath('更新料')).text
            data.occupancy_requirement = self.find_element(By.XPATH, data_xpath('入居条件')).text
            data.equipment_warranty = self.find_element(By.XPATH, data_xpath('設備保証')).text
            data.rent_free = self.find_element(By.XPATH, data_xpath('フリーレント')).text

def data_xpath(str: str, tag: str = 'td', parent: str = '') -> str:
    return f'//{tag}[contains(text(), "{str}")]/{parent}following-sibling::td'

def floor_plan_translate(str: str):
    translate_dict = {
        'ワンルーム': '1R',
        '1SK': '1K',
        '1LK': '1DK',
        '1SDK': '1DK',
        '1SLK': '1DK',
        '1SLDK': '1LDK',
        '2SK': '2K',
        '2LK': '2DK',
        '2SDK': '2DK',
        '2SLK': '2DK',
        '2SLDK': '2LDK',
        '3SK': '3K',
        '3LK': '3DK',
        '3SDK': '3DK',
        '3SLK': '3DK',
        '3SLDK': '3LDK',
        '4SK': '4K',
        '4LK': '4DK',
        '4SDK': '4DK',
        '4SLK': '4DK',
        '4SLDK': '4LDK',
    }
    if str in translate_dict:
        return translate_dict[str]
    return str