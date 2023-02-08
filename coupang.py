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

# 쿠키를 만들어서 활용. subprocess 활용함.
subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
# Navigate to the CoupangLogin homepage
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# 크롬 자동 드라이버 설치 및 버전 맞춤.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
# Navigate to the Google homepage
# url_login = "https://login.coupang.com/login/login.pang"
url = "https://login.coupang.com"
driver.get(url)
##########################################################
# 홈페이지 로그인 관련 코드
# if driver.current_url == url_login:
#     email = driver.find_element(By.NAME, "email")
#     email.send_keys("my_email")
#     password = driver.find_element(By.NAME, "password")
#     time.sleep(3)
#     password.send_keys("my_password")
#     password.send_keys(Keys.ENTER)
#     print("여기가 읽혔어요!")
# print("끝났어용")
###########################################################

# 로그인을 할 경우 뜰 때까지 기다려 줘야함.
driver.implicitly_wait(10)
# Find the search box element and enter a query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("아이패드")
search_box.send_keys(Keys.ENTER)
nameAry = []  # 상품 이름 리스트
priceAry = []  # 상품 가격 리스트
while True:
    datas = driver.find_elements(By.CSS_SELECTOR, ".search-product")
    cnt = 0
    for item in datas:
        try:  # 예외 처리 구문으로
            name = item.find_element(By.XPATH, "a/dl/dd/div/div[2]").text
            price = item.find_element(By.XPATH, "a/dl/dd/div/div[3]/div/div[1]/em/strong").text
            print(name)
            print(price)
        except NoSuchElementException as e:  # 만약 name, price가 엘리멘트가 없을 경우,
            print(f"NoSuchElementError : {e}")
        except Exception as e:  # 모든 에러를 잡기 위해 예외.
            print(f"Anonymous Error : {e}")
        finally:
            cnt += 1
            if cnt % 3 == 1:  # 무조건 3번마다 포인팅하면서 스크롤이 필요하다면 스크롤.
                act = ActionChains(driver)
                act.move_to_element(item).perform()
                time.sleep(0.5)
    # 너무 빨라서 못봐서 해놓음.
    time.sleep(1)
    try:  # 마지막 페이지에 대한 예외처리
        next_page_link = driver.find_element(By.CSS_SELECTOR, '.btn-next')
        next_page_link.click()
    except Exception as e:  # 여러 예외 처리
        print(f"Exception :{e}")
        driver.quit()
        break

# Close the browser window
data = {"product": nameAry, "price": priceAry}  # 딕셔너리로 저장
df = pd.DataFrame(data)
df.to_csv("test.csv", encoding="utf-8-sig")  # csv로 저장.
driver.quit()
