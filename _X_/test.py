from selenium.webdriver.chrome.service import Service
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"
op = webdriver.ChromeOptions()
op.add_argument('headless')

driver = webdriver.Chrome(service=Service(chrome_driver_path),  options=op)

URL = 'https://pythonbasics.org'

driver.get(URL)

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
driver.find_element(By.TAG_NAME, 'body').screenshot('web_screenshot.png')

driver.quit()