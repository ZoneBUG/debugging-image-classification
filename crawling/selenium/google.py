from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request


driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko")       # 검색창 주소로 이동
elem = driver.find_element(By.NAME, "q")                 # 가져올 html 태그 (q)
elem.send_keys("그리마")                              # 검색어 입력
elem.send_keys(Keys.RETURN)                              # 겁색어 입력 후 엔터 처리



# 스크롤 먼저 내려놓기
SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    # 스크롤이 끝까지 내려간 경우
    if new_height == last_height:                               
      try:
        driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()   # 결과 더보기 버튼 있으면 클릭 
      except:
        break                                                     # 결과 더보기 버튼 없으면 break
    last_height = new_height



images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")   # 가져올 html 태그 (rg_i Q4LuWd)


count = 1    # 이미지 파일명 설정용 변수

for image in images:
  try:
    image.click()
    time.sleep(2)  # 이미지 가져올 때까지 2초 delay
    imgUrl = driver.find_element(By.CSS_SELECTOR, ".r48jcc pT0Scc iPVvYb").get_attribute("src")  # 선택한 큰 이미지 src 주소 가져오기
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
    count = count + 1
  except:
    pass



driver.close()  # 웹 브라우저 닫기
