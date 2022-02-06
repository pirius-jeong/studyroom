from django.core.management.base import BaseCommand
from django.utils import timezone

import sqlite3
import pandas as pd
from pandas import Series, DataFrame
from datetime import datetime
from dateutil.relativedelta import relativedelta

from studyroom.models import Bill, Account, Pay

from selenium import webdriver
import chromedriver_autoinstaller
import time
from selenium.webdriver.common.by import By

class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        con = sqlite3.connect("db.sqlite3")
        chromedriver_autoinstaller.install()

        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        driver.set_window_position(0, 0)
        driver.set_window_size(1920, 1080)

        driver.get('https://www.hometax.go.kr/')
        time.sleep(30)

        # 로그인 메뉴 이동
        driver.find_element(By.ID, 'textbox81212912').click()
        time.sleep(10)

        # 본문 iframe 이동
        iframe = driver.find_element(By.XPATH, '//*[@id="txppIframe"]')
        driver.switch_to.frame(iframe)
        time.sleep(10)

        # 아이디 로그인 탭 이동
        driver.find_element(By.XPATH, '//*[@id="group91882156"]').click()
        time.sleep(3)

        # 아이디/비번 입력
        driver.find_element(By.XPATH, '//*[@id="iptUserId"]').send_keys('alrudsim')
        driver.find_element(By.XPATH, '//*[@id="iptUserPw"]').send_keys('#smk445566')
        driver.find_element(By.XPATH, '//*[@id="anchor25"]').click()
        time.sleep(5)

        # 조회/발급 메뉴 이동
        driver.find_element(By.XPATH, '//*[@id="textbox81212923"]').click()
        time.sleep(5)

        # 현금영수증조회 > 매출내역 조회
        iframe = driver.find_element(By.XPATH, '//*[@id="txppIframe"]')
        driver.switch_to.frame(iframe)
        driver.find_element(By.XPATH, '//*[@id="sub_a_0105010000"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="sub_a_0105010600"]').click()
        time.sleep(10)

        # 일별 탭
        #driver.find_element(By.XPATH,'//*[@id="tabControl1_UTECRCB057_tab_tabs1"]/div[1]').click()
        # 주별 탭
        #driver.find_element(By.XPATH, '//*[@id="tabControl1_UTECRCB057_tab_tabs2"]/div[1]').click()
        # 월별 탭
        #driver.find_element(By.XPATH,'//*[@id="tabControl1_UTECRCB057_tab_tabs3"]/div[1]').click()
        # 분기별 탭
        driver.find_element(By.XPATH,'//*[@id="tabControl1_UTECRCB057_tab_tabs4"]/div[1]').click()
        time.sleep(1)

        # 조회하기 클릭
        driver.find_element(By.XPATH, '//*[@id="group1988"]').click()
        time.sleep(5)

        table = driver.find_element(By.XPATH, '//*[@id="grdCshpt_body_table"]/tbody')
        rows = int(driver.find_element(By.XPATH, '//*[@id="txtTotal"]').text)
        pages = rows // 10
        if rows % 10 > 0:
            pages = pages + 1
        row = 0
        page = '//*[@id="pglNavi_page_%s"]'
        pay_type = 'KP'
        pay_status = 'OP'

        for i in range(0, pages):
            for tr in table.find_elements(By.TAG_NAME, 'tr'):
                td = tr.find_elements(By.TAG_NAME, 'td')
                pay_date = td[2].text.replace('-', '').replace(' ', '').replace(':', '')
                pay_amt = int(td[3].text.replace(',', ''))
                payer = td[8].text
                try:
                    account = Account.objects.get(payer_phone_num=payer)
                    pay = Pay(pay_status=pay_status, pay_type=pay_type, pay_date=pay_date, pay_amt=pay_amt, payer=payer, account=account,
                              create_date=timezone.now())
                except:
                    pay = Pay(pay_status=pay_status, pay_type=pay_type, pay_date=pay_date, pay_amt=pay_amt, payer=payer, create_date=timezone.now())
                pay.save()
                row = row + 1
                if row == rows:
                    break
            if row == rows:
                break
            driver.find_element(By.XPATH, page % str(i+2)).click()
            time.sleep(3)