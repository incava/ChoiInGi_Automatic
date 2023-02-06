from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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
# driver.get("https://www.google.com")
# search_box = driver.find_element(By.NAME, "q")
# search_box.send_keys("블랙핑크")
# search_box.send_keys(Keys.ENTER)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# searchAttrFilterattr_12447-1 > ul > li:nth-child(4) > label
driver.get("https://www.coupang.com")
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("아이패드")
search_box.send_keys(Keys.ENTER)
datas = driver.find_elements(By.CSS_SELECTOR, '#searchAttrFilterattr_12447-1 > ul > li:nth-child(3) > label')
for i in datas:
    print(datas)
    i.click() # 아이패드mini 모델 클릭까지 완료!!
#datas.submit()


