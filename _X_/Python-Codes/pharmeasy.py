from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"

op = webdriver.ChromeOptions()
op.add_argument('headless')

medicine_name = input("Enter medicine name: ")

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)

PHARMEASY = f"https://pharmeasy.in"
driver.get(PHARMEASY)
driver.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div/div[1]/div/div[2]/div/div[2]/span").click()

search_box = driver.find_element(By.XPATH, "//*[@id='topBarInput']")
search_box.send_keys(medicine_name)
search_box.send_keys(Keys.RETURN)


medicines_pharmeasy = []
medicines_link = []

medicine_span = driver.find_element(By.CSS_SELECTOR, ".LHS_container__XL4ZP")
medicines_name = medicine_span.find_elements(By.CLASS_NAME, "ProductCard_medicineName__17En6")
medicines_price = medicine_span.find_elements(By.CLASS_NAME, "ProductCard_ourPrice__3fkJf")

for i in range(2, len(medicines_name)+2):
    med_lnks = driver.find_element(By.CSS_SELECTOR, f".LHS_container__XL4ZP > div:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
    medicines_link.append(med_lnks.get_attribute('href'))

for i in range(len(medicines_name)):
    medicine = {}
    medicine.update({"Med-Name": medicines_name[i].text, "Med-Price": medicines_price[i].text[0:-1], "Med-Link": medicines_link[i]})
    medicines_pharmeasy.append(medicine)

print(medicines_pharmeasy)
