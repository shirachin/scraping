from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from webdriver_manager.chrome import ChromeDriverManager


from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import requests



import traceback
import sys
import os
import re
import pprint
import pyperclip
import asyncio

from tool.settings import CHROME_PATH, REWARD_FILTER, API_URL
from tool.search_setting import search_terms
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





RE_M = re.compile(r'[\d.]+ヶ月')
RE_P = re.compile(r'[\d.]+％')
RE_Y = re.compile(r'[\d.]+万円')

class Driver:
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