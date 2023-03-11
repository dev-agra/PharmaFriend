import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"

op = webdriver.ChromeOptions()
op.add_argument('headless')

medicine_name = input("Enter medicine name: ")

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)

APOLLOPHARM = f"https://www.apollopharmacy.in/"
driver.get(APOLLOPHARM)


search_box = driver.find_element(By.CSS_SELECTOR, "#searchProduct")
search_box.send_keys(medicine_name)
search_box.send_keys(Keys.RETURN)

medicines_apollo = []
medicines_link = []

time.sleep(5)
medicines_span = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div")
medicines_name = medicines_span.find_elements(By.CLASS_NAME, "ProductCard_productName__2LhTY")
medicines_price = medicines_span.find_elements(By.CLASS_NAME, "ProductCard_priceGroup__Xriou")

for i in range(len(medicines_name)):
    med_lnks = driver.find_element(By.CSS_SELECTOR, f".ProductCard_pcContainer__2snw3 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child({i+1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
    medicines_link.append(med_lnks.get_attribute('href'))

for i in range(len(medicines_name)):
    medicine = {}
    medicine.update({"Med-Name": medicines_name[i].text, "Med-Price": '₹' + medicines_price[i].text.split('₹')[2], "Med-Link": medicines_link[i]})
    medicines_apollo.append(medicine)

print(medicines_apollo)
