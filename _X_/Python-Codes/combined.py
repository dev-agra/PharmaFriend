import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"

op = webdriver.ChromeOptions()
op.add_argument('headless')


def combined(MEDNAME):
    medicine_name = MEDNAME
    driverA = webdriver.Chrome(service=Service(chrome_driver_path), options=op)  # To get Apollo Pharmacy
    driverN = webdriver.Chrome(service=Service(chrome_driver_path), options=op)  # To get NetMeds
    driverP = webdriver.Chrome(service=Service(chrome_driver_path), options=op)  # To get Pharmeasy

    # To get ApolloPharmacy information

    APOLLOPHARM = f"https://www.apollopharmacy.in/"
    driverA.get(APOLLOPHARM)

    if medicine_name == "Nitrolong 2.6 Tablet CR":
        medicine_name_apollo = medicine_name.split(' ')[0] + ' ' + medicine_name.split(' ')[1]
    else:
        medicine_name_apollo = MEDNAME

    search_box_apollo = driverA.find_element(By.CSS_SELECTOR, "#searchProduct")
    search_box_apollo.send_keys(medicine_name_apollo)
    search_box_apollo.send_keys(Keys.RETURN)

    medicines_apollo = {}
    medicines_link_apollo = []
    medicines_name_apollo_list = []

    time.sleep(5)
    medicines_span_apollo = driverA.find_element(By.XPATH,
                                                 "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div")
    medicines_name_apollo = medicines_span_apollo.find_elements(By.CLASS_NAME, "ProductCard_productName__2LhTY")
    medicines_price_apollo = medicines_span_apollo.find_elements(By.CLASS_NAME, "ProductCard_priceGroup__Xriou")

    for i in range(len(medicines_name_apollo)):
        med_lnks = driverA.find_element(By.CSS_SELECTOR,
                                        f".ProductCard_pcContainer__2snw3 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child({i + 1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
        medicines_link_apollo.append(med_lnks.get_attribute('href'))

    for i in range(len(medicines_name_apollo)):
        try:
            medicines_pr_apollo = '₹' + medicines_price_apollo[i].text.split('₹')[2]
        except:
            medicines_pr_apollo = '₹' + medicines_price_apollo[i].text.split('₹')[1]

        medicines_apollo.update(
            {f'{medicines_name_apollo[i].text}': {"Meddis": medicines_pr_apollo, "Medlink": medicines_link_apollo[i]}})

        medicines_name_apollo_list.append(medicines_name_apollo[i].text)

    apollomeds = medicines_apollo

    # To get NetMeds Information
    NETMEDS = f"https://www.netmeds.com/"
    driverN.get(NETMEDS)

    search_box_netmeds = driverN.find_element(By.XPATH, "//*[@id='search']")
    search_box_netmeds.send_keys(medicine_name)
    search_box_netmeds.send_keys(Keys.RETURN)
    medicines_netmeds_main = {}
    medicines_name_netmeds_list = []

    time.sleep(5)
    medicine_span_netmeds = driverN.find_element(By.CSS_SELECTOR, "#algolia_hits")
    medicines_netmeds = medicine_span_netmeds.find_elements(By.CLASS_NAME, "ais-InfiniteHits-item")

    time.sleep(5)
    for i in range(len(medicines_netmeds)):
        med_name = driverN.find_element(By.CSS_SELECTOR,
                                        f"li.ais-InfiniteHits-item:nth-child({i + 1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > div:nth-child(1)").text
        try:
            med_price_dis = driverN.find_element(By.CSS_SELECTOR,
                                                 f"li.ais-InfiniteHits-item:nth-child({i + 1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(6) > span:nth-child(2)").text
        except:
            med_price_dis = driverN.find_element(By.CSS_SELECTOR,
                                                 f"li.ais-InfiniteHits-item:nth-child({i + 1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(5) > span:nth-child(2)").text

        med_link = driverN.find_element(By.CSS_SELECTOR,
                                        f"li.ais-InfiniteHits-item:nth-child({i + 1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)").get_attribute(
            'href')

        medicines_netmeds_main.update({f'{med_name}': {"Meddis": med_price_dis, "Medlink": med_link}})
        medicines_name_netmeds_list.append(med_name)

    netmedsmeds = medicines_netmeds_main

    # To get PharmEasy Information
    PHARMEASY = f"https://pharmeasy.in"
    driverP.get(PHARMEASY)
    driverP.find_element(By.XPATH, "//*[@id='__next']/main/div[3]/div[1]/div/div[1]/div/div[2]/div/div[2]/span").click()

    search_box_pharm = driverP.find_element(By.XPATH, "//*[@id='topBarInput']")
    search_box_pharm.send_keys(medicine_name)
    search_box_pharm.send_keys(Keys.RETURN)

    medicines_pharmeasy = {}
    medicines_link_pharm = []
    medicines_name_pharm_list = []

    medicine_span_pharm = driverP.find_element(By.CSS_SELECTOR, ".LHS_container__XL4ZP")
    medicines_name_pharm = medicine_span_pharm.find_elements(By.CLASS_NAME, "ProductCard_medicineName__17En6")
    medicines_price_pharm = medicine_span_pharm.find_elements(By.CLASS_NAME, "ProductCard_ourPrice__3fkJf")

    for i in range(2, len(medicines_name_pharm) + 2):
        med_lnks_pharm = driverP.find_element(By.CSS_SELECTOR,
                                              f".LHS_container__XL4ZP > div:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
        medicines_link_pharm.append(med_lnks_pharm.get_attribute('href'))

    for i in range(len(medicines_name_pharm)):
        medicine = {}
        medicines_pharmeasy.update({f'{medicines_name_pharm[i].text}': {"Meddis": medicines_price_pharm[i].text[0:-1],
                                                                        "Medlink": medicines_link_pharm[i]}})
        medicines_name_pharm_list.append(medicines_name_pharm[i].text)

    pharmmeds = medicines_pharmeasy

    driverA.quit()
    driverN.quit()
    driverP.quit()

    return apollomeds, medicines_name_apollo_list, netmedsmeds, medicines_name_netmeds_list, pharmmeds, medicines_name_pharm_list


med_name = input("Enter medicine name: ")

x, a, y, b, z, c = combined(med_name)

print(a)
xm = input("Enter medicine name: ")
print(x[xm])
