import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# 저장 경로
current_path = os.getcwd()
# 원하는 검색어 및 이미지 개수
inserturl = input("검색어를 입력하세요 : ").strip()

driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(3)
driver.get("https://www.google.co.kr/imghp?hl=ko")
elem = driver.find_element(By.NAME, "q")                 # 가져올 html 태그 (q)
elem.send_keys("그리마")                              # 검색어 입력
elem.send_keys(Keys.RETURN)      

SCROLL_PAUSE_TIME = 1

# 현재 브라우저의 높이
last_height = driver.execute_script(
    "return document.body.scrollHeight")  # 브라우져 높이를 확인 가능(자바스크립트)

# 검색 화면에서 스크롤을 끝까지 내려 관련 이미지 전부를 가져옵니다.
while True:
    # Scroll down to bottom
    # 브라우져 끝까지 스크롤을 내리겠다.
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(new_height)

    if new_height == last_height:
        try:
            # 화면 맨 아래 펼쳐보기 버튼 클릭
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click() 
        except:
            print("error")
            break
    last_height = new_height

# 복수 이미지 정보를 가져옵니다 list 형  * find_elements 를 사용합니다.
images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")

# 폴더 명도 검색어랑 동일하게 세팅 !
folder_name = inserturl

# 폴더 있는지 없는지 확인 후 생성
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

# 이미지 다운로드 !
count = 1 
for image in images:
  try:
    image.click()
    time.sleep(2)  # 이미지 가져올 때까지 2초 delay
    imgUrl = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]").get_attribute("src")  # 선택한 큰 이미지 src 주소 가져오기
    opener=urllib.request.build_opener()
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
    count = count + 1
  except:
    print("error")
    pass
driver.close()