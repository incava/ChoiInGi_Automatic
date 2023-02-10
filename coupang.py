import sys
import threading
import time
import subprocess
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class Pasing:
    # 필터값을 설정 하기 위해 생성자를 받도록함.
    def __init__(self, url, search_name, min_price=0, max_price=None, contain_names=None):
        if contain_names is None:
            contain_names = []
        self.contain_names = contain_names
        self.url = url
        self.search_name = search_name
        self.min_price = min_price
        self.max_price = max_price
        self.nameAry = []  # 상품 이름 리스트
        self.priceAry = []  # 상품 가격 리스트
        subprocess.Popen(
            r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
        # Navigate to the CoupangLogin homepage
        option = Options()
        option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # 크롬 자동 드라이버 설치 및 버전 맞춤.
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    def ary_clear(self):
        self.nameAry.clear()
        self.priceAry.clear()

    def set_instance(self, url, search_name, min_price, max_price, contain_names):
        self.contain_names = contain_names
        self.url = url
        self.search_name = search_name
        self.min_price = min_price
        self.max_price = max_price

    def filter_price(self, price):
        # 범위값 안에 드는지 확인 후 리턴.
        price = int(price.replace(",", ""))
        return self.min_price <= price <= self.max_price

    def filter_names(self, name):
        def name_check():
            for i in self.contain_names:
                if i not in name:
                    return False
            return True

        # 만약 원하는 필터가 없다면 True
        if len(self.contain_names) == 0:
            return True
        # print(f"filter_names: {name_check()}")
        return name_check()
        # 필더가 있다면 확인

    def auto_start(self):
        self.ary_clear()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        # Find the search box element and enter a query
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(self.search_name)
        search_box.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(10)
        while True:
            # 상품이 가지고 있는 속성 css
            datas = self.driver.find_elements(By.CSS_SELECTOR, ".search-product")
            cnt = 0
            for item in datas:
                try:  # 예외 처리 구문으로
                    name = item.find_element(By.XPATH, "a/dl/dd/div/div[2]").text
                    price = item.find_element(By.XPATH, "a/dl/dd/div/div[3]/div/div[1]/em/strong").text
                    # 만약 filter에 적합하다면 append
                    if self.filter_names(name) and self.filter_price(price):
                        self.nameAry.append(name)
                        self.priceAry.append(price)
                        print(name)
                        print(price)
                except NoSuchElementException as e:  # 만약 name, price가 엘리멘트가 없을 경우,
                    print(f"NoSuchElementError : {e}")
                except Exception as e:  # 모든 에러를 잡기 위해 예외.
                    print(f"Anonymous Error : {e}")
                finally:
                    cnt += 1
                    if cnt % 3 == 1:  # 무조건 3번마다 포인팅하면서 스크롤이 필요하다면 스크롤.
                        act = ActionChains(self.driver)
                        act.move_to_element(item).perform()
                        time.sleep(0.5)
            # 너무 빨라서 못봐서 해놓음.
            time.sleep(1)
            try:  # 마지막 페이지에 대한 예외 처리
                next_page_link = self.driver.find_element(By.CSS_SELECTOR, '.btn-next')
                next_page_link.click()
            except Exception as e:  # 여러 예외 처리
                print(f"Exception :{e}")
                self.driver.quit()
                break
        data = {"product": self.nameAry, "price": self.priceAry}  # 딕셔너리로 저장
        df = pd.DataFrame(data)
        df.to_csv("test.csv", encoding="utf-8-sig")  # csv로 저장.
        self.driver.quit()


