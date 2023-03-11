from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"

op = webdriver.ChromeOptions()
op.add_argument('headless')

medicine_name = input("Enter medicine name: ")

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)

NETMEDS = f"https://www.netmeds.com/"
driver.get(NETMEDS)

search_box = driver.find_element(By.XPATH, "//*[@id='search']")
search_box.send_keys(medicine_name)
search_box.send_keys(Keys.RETURN)


medicines_netmeds = []

medicine_span = driver.find_element(By.CSS_SELECTOR, "#algolia_hits")
medicines = medicine_span.find_elements(By.CLASS_NAME, "ais-InfiniteHits-item")

for i in range(len(medicines)):
    medicine = {}
    med_name = driver.find_element(By.CSS_SELECTOR, f"li.ais-InfiniteHits-item:nth-child({i+1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > div:nth-child(1)").text
    med_price_mrp = driver.find_element(By.CSS_SELECTOR, f"li.ais-InfiniteHits-item:nth-child({i+1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(6) > span:nth-child(3) > strike:nth-child(1)").text
    med_price_dis = driver.find_element(By.CSS_SELECTOR, f"li.ais-InfiniteHits-item:nth-child({i+1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(6) > span:nth-child(2)").text
    med_link = driver.find_element(By.CSS_SELECTOR, f"li.ais-InfiniteHits-item:nth-child({i+1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)").get_attribute('href')
    medicine.update({"Med-Name": med_name, "Med-MRP": med_price_mrp, "Med-DIS": med_price_dis, "Med-Link": med_link})
    medicines_netmeds.append(medicine)

print(medicines_netmeds)
