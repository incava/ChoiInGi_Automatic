import time
import re
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class Pasing:
    # 필터값을 설정 하기 위해 생성자를 받도록함.
    def __init__(self):
        self.__name_array = []  # 상품 이름 리스트
        self.__price_array = []  # 상품 가격 리스트
        self.__thread = False
        self.__progress_info__ = "반갑습니다."

    @property
    def thread(self):
        return self.__thread

    @thread.setter
    def thread(self, value: bool):
        self.__thread = value

    @property
    def name_array(self):
        return self.__name_array

    @name_array.setter
    def name_array(self, value):
        self.__name_array = value

    @property
    def price_array(self):
        return self.__price_array

    @price_array.setter
    def price_array(self, value):
        self.__price_array = value

    def set_path(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument("disable-gpu")
        option.add_argument("--lang=ko_KR")
        option.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("--disable-extensions")
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        # 크롬 자동 드라이버 설치 및 버전 맞춤.
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        driver.minimize_window()
        return driver

    def ary_clear(self):
        self.name_array.clear()
        self.price_array.clear()

    def progress_clear(self):
        self.__progress_info__ = ""

    @staticmethod
    def filter_price(price, min_price, max_price):
        # 범위값 안에 드는지 확인 후 리턴.
        price = int(re.sub('[^0-9]', '', price))
        print(price)
        return min_price <= price <= max_price

    @staticmethod
    def filter_names(name, contain_names):
        def name_check():
            for keyword in contain_names:
                # 대, 소문자 구분 때문에
                if str(keyword).upper() not in name and str(keyword).lower() not in name:
                    return False
            return True

        # 만약 원하는 필터가 없다면 True
        if len(contain_names) == 0:
            return True
        return name_check()
        # 필더가 있다면 확인

    def auto_start(self, url, search_name, min_price, max_price, filter_array):
        # 예기치 못한 상황이라면 error+msg, 성공적이면 success, 실패라면 fail, 종료를 원했다면 exit
        driver = self.set_path()

        self.ary_clear()
        driver.get(url)
        driver.implicitly_wait(10)
        # Find the search box element and enter a query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_name)
        search_box.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        while True:
            # 상품이 가지고 있는 속성 css
            datas = driver.find_elements(By.CSS_SELECTOR, ".search-product")
            cnt = 0
            for item in datas:
                if self.__thread:  # 사용자가 원하는 종료
                    driver.quit()
                    self.__thread = False
                    return 'exit'
                try:  # 예외 처리 구문으로
                    name = item.find_element(By.XPATH, "a/dl/dd/div/div[2]").text
                    price = item.find_element(By.XPATH, "a/dl/dd/div/div[3]/div/div[1]/em").text
                    # 만약 filter에 적합하다면 append
                    if self.filter_names(name, filter_array) and self.filter_price(price, min_price, max_price):
                        self.name_array.append(name)
                        self.price_array.append(price)
                        self.__progress_info__ += name + '\n'
                        self.__progress_info__ += price + '\n'
                        print(self.__progress_info__)
                        print(price)
                except NoSuchElementException as e:  # 만약 name, price가 엘리멘트가 없을 경우,
                    print(f"NoSuchElementError : {e}")
                except Exception as e:  # 모든 에러를 잡기 위해 예외.
                    print(f"Anonymous Error : {e}")
                    return 'error: ' + str(e)  # 예기치 못한 상황에 대한 종료
                finally:
                    cnt += 1
                    if cnt % 3 == 1:  # 무조건 3번마다 포인팅하면서 스크롤이 필요하다면 스크롤.
                        act = ActionChains(driver)
                        act.move_to_element(item).perform()
                        time.sleep(0.5)
            # 너무 빨라서 못봐서 해놓음.
            time.sleep(1)
            try:  # 마지막 페이지에 대한 예외 처리
                next_page_link = driver.find_element(By.CSS_SELECTOR, '.btn-next')
                next_page_link.click()
            except NoSuchElementException as e:  # 만약 next_page_link가 더이상 없다면
                return 'success'
            except Exception as e:  # 여러 예외 처리
                driver.quit()
                return 'error: ' + str(e)

    def ary_to_csv(self):
        try:
            data = {"product": self.name_array, "price": self.price_array}  # 딕셔너리로 저장
            df = pd.DataFrame(data)
            df.to_csv("test.csv", encoding="utf-8-sig")  # csv로 저장.
            return 'success'
        except Exception as e:
            return 'error: ' + str(e)
