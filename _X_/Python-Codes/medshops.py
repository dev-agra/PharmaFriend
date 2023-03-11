from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"
op = webdriver.ChromeOptions()
op.add_argument('headless')


def getgovdist():
    driver = webdriver.Chrome(service=Service(chrome_driver_path))

    weblink = "http://janaushadhi.gov.in/KendraDetails.aspx"

    # To get state details
    driver.get(weblink)
    time.sleep(1)
    states = []
    state_value = driver.find_element(By.XPATH, "//*[@id='Bppi_body_ddlState']")
    state = Select(state_value)

    for opt in state.options:
        states.append(opt.text)

    #     Insert state name here
    state.select_by_visible_text("Maharashtra")
    time.sleep(1)

    districts_list = []
    dist_value = driver.find_element(By.XPATH, "//*[@id='Bppi_body_ddlDistrict']")
    district_webobject = Select(dist_value)
    for opt in district_webobject.options:
        districts_list.append(opt.text)

    driver.quit()
    return districts_list, district_webobject


def getgovmeds(statename, district_name):
    driver = webdriver.Chrome(service=Service(chrome_driver_path))

    weblink = "http://janaushadhi.gov.in/KendraDetails.aspx"
    driver.get(weblink)

    state_value = driver.find_element(By.XPATH, "//*[@id='Bppi_body_ddlState']")
    state = Select(state_value)

    state.select_by_visible_text(statename)
    time.sleep(1)

    dist_value = driver.find_element(By.XPATH, "//*[@id='Bppi_body_ddlDistrict']")
    district = Select(dist_value)

    district.select_by_value(district_name)
    time.sleep(1)
    search_button = driver.find_element(By.XPATH, "//*[@id='Bppi_body_btnSearch']")
    search_button.click()

    # To get info of Shop details in selected District
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    kendra = soup.find('table', class_='table table-striped table-bordered table-hover')

    blank = []
    for kendra_row in kendra.find_all('tr'):
        heads = kendra_row.find_all('th')
        for head in heads:
            kendra_names = head.text
            blank.append(kendra_names)

    split_data = [blank[x:x+7] for x in range(0, len(blank), 7)]

    gov_shops = []
    for i in range(len(split_data)):
        spare = {}
        kendra_no = split_data[i][0]
        kendra_code = split_data[i][1]
        kendra_district = split_data[i][2]
        kendra_address = split_data[i][3]
        kendra_person = split_data[i][5]
        kendra_status = split_data[i][6]
        spare.update({"kendra_no": kendra_no, "kendra_code": kendra_code, "kendra_district": kendra_district, "kendra_address": kendra_address, "kendra_person": kendra_person, "kendra_status": kendra_status})
        gov_shops.append(spare)

    driver.quit()
    return gov_shops

sname = input("Enter statename: ")
dname = input("Enter districtname" )

z = getgovmeds(sname, dname)
print(z)
