import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
# 크롬 브라우저 꺼짐 방지 옵션
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
# 크롤링 방지 설정을 undefined로 변경
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
})
# Navigate to the Google homepage
driver.get("https://www.coupang.com")
# Find the search box element and enter a query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("아이패드")
search_box.send_keys(Keys.ENTER)
nameAry = []
priceAry = []

# datas = driver.find_elements(By.CSS_SELECTOR, ".search-product")  -> 데이터가 담긴 class
# #\36 396408893 > a > dl > dd > div > div.name // 이름 css
# #\36 091182002 > a > dl > dd > div > div.name
# #\36 396408893 > a > dl > dd > div > div.price-area > div > div.price > em > strong //가격 css
while True:
    datas = driver.find_elements(By.CSS_SELECTOR, ".search-product")
    for item in datas:
        name = item.find_element(By.CSS_SELECTOR, ".name").text
        price = item.find_element(By.CSS_SELECTOR, ".price-value").text
        if name is None or price is None:  # 하나라도 없는게 있더라.. 그래서 예외처리 해줌. 그냥 넘어가
            continue
        nameAry.append(name)
        priceAry.append(price)
        print(name)
        print(price)
    try:  # 마지막 페이지에 대한 예외처리
        next_page_link = driver.find_element(By.CSS_SELECTOR, '.btn-next')
        next_page_link.click()
    except:
        break
    # 너무 빨라서 못봐서 해놓음.
    time.sleep(1)
# Close the browser window
data = {"product": nameAry, "price": priceAry} #딕셔너리로 저장
df = pd.DataFrame(data)
df.to_csv("test.csv", encoding="utf-8-sig") # csv로 저장.
driver.quit()
