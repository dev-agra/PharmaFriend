import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import random
from pathlib import Path
import os

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"
op = webdriver.ChromeOptions()
op.add_argument('headless')
op.add_argument('disable-popup-blocking')
BASE_DIR = Path(__file__).resolve().parent.parent

def didyoumean(medname):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('disable-popup-blocking')

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)
    medicine_name = medname
    ONEMG = f"https://www.1mg.com/"
    driver.get(ONEMG)

    # Send Search keys
    search_box = driver.find_element(By.XPATH, "//*[@id='srchBarShwInfo']")
    search_box.send_keys(medicine_name)
    search_box.send_keys(Keys.RETURN)

    # Function to scroll to EOP
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Get the name of Medicines style__pro-title___3G3rr
    names = driver.find_elements(By.CLASS_NAME, "style__pro-title___3zxNC")

    # If in case we try to access medicine which has more than 20 types/variants
    if len(names) == 0:
        names = driver.find_elements(By.CLASS_NAME, "style__pro-title___3G3rr")

    products = []
    for p in names:
        products.append(p.text)

    # Get list of links of medicines
    medicine_links = []
    medicine_mrp = []

    try:
        root_med_link = driver.find_element(By.CSS_SELECTOR,
                                            "div.col-xs-12:nth-child(1) > div:nth-child(1) > a:nth-child(1)")

        root_med_mrp = driver.find_element(By.CSS_SELECTOR,
                                           "div.col-xs-12:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(3) > div:nth-child(1)").text
        root_med_mrp = '₹' + root_med_mrp.split('₹')[1]
        if len(root_med_mrp.split('\n')) > 1:
            root_med_mrp = '₹' + root_med_mrp.split('₹')[1].split('\n')[0]
        medicine_mrp.append(root_med_mrp)
        root_med = "xs"

    except NoSuchElementException:
        root_med_link = driver.find_element(By.CSS_SELECTOR,
                                            "div.col-sm-4:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
        try:
            root_med_mrp = driver.find_element(By.CSS_SELECTOR,
                                               "div.col-sm-4:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)").text
        except:
            root_med_mrp = driver.find_element(By.CSS_SELECTOR,
                                               "div.col-sm-4:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(6) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)").text

        root_med_mrp = '₹' + root_med_mrp.split('₹')[1]
        medicine_mrp.append(root_med_mrp)
        root_med = "sm"

    href_link = root_med_link.get_attribute("href")
    medicine_links.append(href_link)

    if root_med == 'xs':
        for i in range(2, len(products) + 1):
            med_link = driver.find_element(By.CSS_SELECTOR,
                                           f"div.style__container___cTDz0:nth-child({i}) > div:nth-child(1) > a:nth-child(1)")

            try:
                med_mrp = driver.find_element(By.CSS_SELECTOR,
                                              f"div.style__container___cTDz0:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(3) > div:nth-child(1)").text
                med_mrp = '₹' + med_mrp.split('₹')[1]
                if len(med_mrp.split('\n')) > 1:
                    med_mrp = '₹' + med_mrp.split('₹')[1].split('\n')[0]
            except:
                try:
                    med_mrp = driver.find_element(By.CSS_SELECTOR,
                                                  f"div.col-xs-12:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(3) > div:nth-child(1)").text
                    med_mrp = '₹' + med_mrp.split('₹')[1]
                    print(2)
                except:
                    print(3)
                    med_mrp = driver.find_element(By.CSS_SELECTOR, f".style__discount-price___-Cikw").text
                    med_mrp = '₹' + med_mrp.split('₹')[1]
            medicine_mrp.append(med_mrp)
            href_link_temp = med_link.get_attribute("href")
            medicine_links.append(href_link_temp)

    if root_med == 'sm':
        for i in range(2, len(products) + 1):
            med_link = driver.find_element(By.CSS_SELECTOR,
                                           f"div.col-md-3:nth-child({i}) > div:nth-child(1) > a:nth-child(1)")
            try:
                med_mrp = driver.find_element(By.CSS_SELECTOR,
                                              f"div.col-md-3:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)").text
                medicine_mrp.append('₹' + med_mrp.split('₹')[1])
                print('0', med_mrp)
            except:
                # div.col-md-3:nth-child(2) > div:nth-child(1) > a:nth-child(1) > div:nth-child(5) > div:nth-child(1)
                try:
                    med_mrp = driver.find_element(By.CSS_SELECTOR,
                                                  f"div.col-md-3:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)").text
                    print('1', med_mrp)
                except:
                    try:
                        med_mrp = driver.find_element(By.CSS_SELECTOR,
                                                      f"div.col-md-3:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(5) > div:nth-child(1)").text
                        if len(med_mrp.split('.')) == 2:
                            med_mrp = driver.find_element(By.CSS_SELECTOR,
                                                          f"div.col-md-3:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(7) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)").text
                        if len(med_mrp.split('₹')) == 2:
                            med_mrp = '₹' + med_mrp.split('₹')[1]
                        print('2', med_mrp)
                    except:
                        med_mrp = driver.find_element(By.CSS_SELECTOR,
                                                      f"div.col-md-3:nth-child({i}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(6) > div:nth-child(1)").text
                        med_mrp = '₹' + med_mrp.split('₹')[1].split('\n')[0].split('%')[0]
                        print('3', med_mrp)

                if len(med_mrp.split('\n')) > 1:
                    med_mrp = '₹' + med_mrp.split('₹')[1].split('\n')[0].split('%')[0]

                medicine_mrp.append(med_mrp)
            href_link_temp = med_link.get_attribute("href")
            medicine_links.append(href_link_temp)
    

    onemg_meds_select = {}

    for i in range(len(products)):
        onemg_meds_select.update({f'{products[i]}': medicine_links[i]})

    onemg_meds_list = []
    for i in range(len(products)):
        onemg_meds = {}
        onemg_meds.update({'medname': products[i], 'medmrp': medicine_mrp[i]})
        onemg_meds_list.append(onemg_meds)

    driver.quit()
    return onemg_meds_list, onemg_meds_select

def getinfo_onemg(ONEMG):
    medinfo = {}
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('disable-popup-blocking')

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)

    # Getting on to the webpage
    LINK = ONEMG
    driver.get(LINK)

    # To get Medicine Name
    flag_med = 0
    try:
        medname = driver.find_element(By.CSS_SELECTOR, ".DrugHeader__title-content___2ZaPo").text
    # When a different medicine appears which gives error
    except:
        medname = driver.find_element(By.CSS_SELECTOR, ".ProductTitle__product-title___3QMYH").text
        flag_med = 1

    if flag_med == 1:
        medname = driver.find_element(By.CSS_SELECTOR, ".ProductTitle__product-title___3QMYH").text
        src = driver.find_element(By.CSS_SELECTOR, ".col-xs-10 > div:nth-child(1) > img:nth-child(1)").get_attribute(
            'src')

        medicineinfo = driver.find_element(By.CSS_SELECTOR, ".ProductDescription__description-content___A_qCZ").text

        medicine_info = medicineinfo.split('\n\n')[0]
        medpricemrp = driver.find_element(By.CSS_SELECTOR, ".PriceBoxPlanOption__margin-right-4___2aqFt").text
        medpricedis = driver.find_element(By.CSS_SELECTOR,
                                          "div.PriceBoxPlanOption__flex___3c7VS:nth-child(1) > div:nth-child(2) > span:nth-child(1)").text

        try:
            medicine_uses_temp = medicineinfo.split('\n\n')[2].split(':')[1].split('\n')[1::]
        except:
            medicine_uses_temp = ["Not Available"]

        medicine_uses = []
        for i in range(len(medicine_uses_temp)):
            med_temp = {}
            med_temp.update({"meduseshead": '', "medusestext": medicine_uses_temp[i]})
            medicine_uses.append(med_temp)

        try:
            medicine_safety = medicineinfo.split('\n\n')[4].split(':')[1].split('\n')[1::]
        except:
            medicine_safety = ["Not Available"]

        medinfo.update({"medlink": LINK,"medname": medname, "medimg": src, "medinfo": medicine_info, "medpricedis": medpricedis,
                        "medpricemrp": medpricemrp, "meduses": medicine_uses,
                        "medeffectspara": "Not Available", "medeffectslist": ["Not Available"],
                        "medmech": "Not Available", "medsafety": medicine_safety, "medalt": ["Not Available"]})

    elif flag_med == 0:
        # To get Medicine image
        try:
            try:
                img = driver.find_element(By.CSS_SELECTOR,
                                          ".style__with-dots___hn8wp > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)")
                src = img.get_attribute('src')
            except:
                img = driver.find_element(By.CSS_SELECTOR, ".col-xs-10 > div:nth-child(1) > img:nth-child(1)")
                src = img.get_attribute('src')
        except:
            src = "Not Available"

        # To get Medicine Info
        medicine_info = driver.find_element(By.CSS_SELECTOR,
                                            "#overview > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)").text
        medicine_info = ''.join(medicine_info.split('\n\n')[:2:])

        try:
            driver.find_element(By.CSS_SELECTOR, "div.ShowMoreArray__toggle___3yZBW:nth-child(1)").click()
        except:
            pass

        # To get Medicine price
        try:
            try:
                medicine_price_dis = driver.find_element(By.CSS_SELECTOR,
                                                         "div.PriceBoxPlanOption__flex___3c7VS:nth-child(1) > div:nth-child(2) > span:nth-child(1)").text
            except NoSuchElementException:
                medicine_price_dis = driver.find_element(By.CSS_SELECTOR, ".DrugPriceBox__best-price___32JXw").text
        except:
            try:
                medicine_price_dis = driver.find_element(By.CSS_SELECTOR, ".DrugPriceBox__price___dj2lv").text
            except:
                medicine_price_dis = "Not Available"

        # To get Medicine Discount price
        if medicine_price_dis != "Not Available":
            try:
                medicine_price_mrp = driver.find_element(By.CSS_SELECTOR,
                                                         ".PriceBoxPlanOption__margin-right-4___2aqFt").text.strip()
            except:
                medicine_price_mrp = driver.find_element(By.CSS_SELECTOR,
                                                         ".DrugPriceBox__slashed-price___2UGqd").text.strip()
        else:
            medicine_price_mrp = "Not Available"

        # To get Medicine Uses
        medicine_uses = []
        info_panel = driver.find_elements(By.CLASS_NAME, "ShowMoreArray__tile___2mFZk")
        for infos in info_panel:
            temp_dict = {}
            info_head = infos.find_element(By.TAG_NAME, 'h3').text
            info_text = infos.find_element(By.TAG_NAME, 'div').text
            info_text = "".join(info_text.split('\n')[1::])
            temp_dict.update({"meduseshead": info_head, "medusestext": info_text})
            medicine_uses.append(temp_dict)

        # To get Medicine Side Effects -> a small paragraph
        medicine_effect_info = driver.find_element(By.CSS_SELECTOR,
                                                   "#side_effects > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)").text

        # To get Medicine Side Effects -> list
        medicine_side_effects = []
        side_effects = driver.find_element(By.CSS_SELECTOR, ".DrugOverview__list-container___2eAr6 > ul:nth-child(1)")
        side_effect_list = side_effects.find_elements(By.TAG_NAME, 'li')
        for effects in side_effect_list:
            medicine_side_effects.append(effects.text)

        # To get Medicine mechanism
        try:
            medicine_mechanism = driver.find_element(By.CSS_SELECTOR,
                                                     "#how_drug_works > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)").text
        except NoSuchElementException:
            medicine_mechanism = "Not Available"

        # To get Medicine Safety Instructions
        medicine_safety = []
        medicine_safety_span = driver.find_element(By.CSS_SELECTOR,
                                                   "#safety_advice > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)")
        medicine_safe_div = medicine_safety_span.find_elements(By.CLASS_NAME, "DrugOverview__warning-top___UD3xX")
        for spans in medicine_safe_div:
            span_text = spans.find_element(By.TAG_NAME, 'span').text
            medicine_safety.append(span_text)

        # To get Medicine Alternatives
        medicine_alternatives = []
        # Adding a "drug-substitute" inside the medicine link to get alternatives
        alternative_link = ONEMG.split('/')
        alternative_link.insert(3, alternative_link[3] + '-substitutes')
        alternative_link.remove('drugs')
        MEDSUBS = '/'.join(alternative_link)

        flag = 0
        # getting the alternative webpage
        driver.get(MEDSUBS)
        try:
            alternative_ul = driver.find_element(By.CSS_SELECTOR, "#srchRslt")
        except:
            flag = 1

        if flag == 0:
            alternative_ul = driver.find_element(By.CSS_SELECTOR, "#srchRslt")
            alternatives = alternative_ul.find_elements(By.TAG_NAME, 'li')
            for i in range(2, len(alternatives)):
                alternative_dict = {}
                alternatives_A = driver.find_element(By.CSS_SELECTOR,
                                                     f"li.list-item:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
                alternatives_medname = alternatives_A.text
                alternatives_link = alternatives_A.get_attribute('href')
                alternatives_tablets = driver.find_element(By.CSS_SELECTOR,
                                                           f"li.list-item:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)").text
                alternatives_pharma = driver.find_element(By.CSS_SELECTOR,
                                                          f"li.list-item:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)").text
                try:
                    alternatives_price = driver.find_element(By.CSS_SELECTOR,
                                                             f"li.list-item:nth-child({i}) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > span:nth-child(2)").text
                except NoSuchElementException:
                    alternatives_price = driver.find_element(By.CSS_SELECTOR,
                                                             f"li.list-item:nth-child({i}) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2) > span:nth-child(4)").text

                alternatives_save = driver.find_element(By.CSS_SELECTOR,
                                                        f"li.list-item:nth-child({i}) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)").text
                # li.list-item:nth-child(15) > div:nth-child(1) > div:nth-child(3) > div:nth-child(3)
                if len(alternatives_save.split('MRP')) == 2:
                    alternatives_save = '₹' + alternatives_save.split('MRP')[1].split('₹')[1]
                    if medicine_price_mrp != "Not Available":
                        alternatives_save = round(((round(float(medicine_price_mrp.split('₹')[1])) - round(
                            float(alternatives_save.split('₹')[1]))) / round(
                            float(medicine_price_mrp.split('₹')[1]))) * 100)
                        if alternatives_save < 0:
                            alternatives_save = f'pay {alternatives_save}% more per Tablet'
                        elif alternatives_save > 0:
                            alternatives_save = f'save {alternatives_save}% more per Tablet'

                alternative_dict.update({"medname": alternatives_medname, "medmanuf": alternatives_pharma,
                                         "medprice": alternatives_price, "medsave": alternatives_save,
                                         "medtablets": alternatives_tablets,
                                         "medlink": alternatives_link})
                medicine_alternatives.append(alternative_dict)

        elif flag == 1:
            medicine_alternatives = ["Not Available"]

        medinfo.update({"medlink": LINK,"medname": medname, "medimg": src, "medinfo": medicine_info, "medpricedis": medicine_price_dis,
                        "medpricemrp": medicine_price_mrp, "meduses": medicine_uses,
                        "medeffectspara": medicine_effect_info, "medeffectslist": medicine_side_effects,
                        "medmech": medicine_mechanism, "medsafety": medicine_safety, "medalt": medicine_alternatives})

    driver.quit()
    return medinfo

def combined(MEDNAME):
    medicine_name = MEDNAME
    print(medicine_name)
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

    # To get link of apollo medicines
    medicines_link_apollo = []

    # To save list of names of apollo medicines
    medicines_name_apollo_list = []

    time.sleep(5)
    
    medicines_span_apollo = driverA.find_element(By.XPATH,
                                                 "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div")
    medicines_name_apollo = medicines_span_apollo.find_elements(By.CLASS_NAME, "ProductCard_productName__f82e9")
    medicines_price_apollo = medicines_span_apollo.find_elements(By.CLASS_NAME, "ProductCard_priceGroup__V3kKR")

    for i in range(len(medicines_name_apollo)):
        med_lnks = driverA.find_element(By.CSS_SELECTOR,
                                        f".ProductCard_pcContainer__S65ur > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child({i + 1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
        medicines_link_apollo.append(med_lnks.get_attribute('href'))

    # To get price of medicine on apollo
    for i in range(len(medicines_name_apollo)):
        try:
            medicines_pr_apollo = '₹' + medicines_price_apollo[i].text.split('₹')[2]
        except:
            medicines_pr_apollo = '₹' + medicines_price_apollo[i].text.split('₹')[1]

        # To store dict of medicines
        medicines_apollo.update(
            {f'{medicines_name_apollo[i].text}': {"Meddis": medicines_pr_apollo, "Medlink": medicines_link_apollo[i]}})

        # To store a list of names of medicines found on apollo pharmacy
        medicines_name_apollo_list.append(medicines_name_apollo[i].text)

    for medicines in medicines_name_apollo_list:
        if str(medicine_name_apollo).split(' ')[0] in medicines.split(' ') and str(medicine_name_apollo).split(' ')[1] in medicines.split(' '):
            pass

    # Final store variable returend by function
    apollomeds = medicines_apollo

    # To get NetMeds Information
    NETMEDS = f"https://www.netmeds.com/"
    driverN.get(NETMEDS)

    search_box_netmeds = driverN.find_element(By.XPATH, "//*[@id='search']")

    netmeds_name = medicine_name.split(" ")[0]

    search_box_netmeds.send_keys(netmeds_name)
    search_box_netmeds.send_keys(Keys.RETURN)
    medicines_netmeds_main = {}
    medicines_name_netmeds_list = []

    time.sleep(5)
    medicine_span_netmeds = driverN.find_element(By.CSS_SELECTOR, "#algolia_hits")
    medicines_netmeds = medicine_span_netmeds.find_elements(By.CLASS_NAME, "ais-InfiniteHits-item")

    time.sleep(5)
    for i in range(len(medicines_netmeds)):
        med_name = driverN.find_element(By.CSS_SELECTOR,
                                        f"li.ais-InfiniteHits-item:nth-child({i + 1}) > div:nth-child(1) > a:nth-child(1) > span:nth-child(3)").text
        try:
            med_price_dis = driverN.find_element(By.CSS_SELECTOR,
                                                 f"li.ais-InfiniteHits-item:nth-child({i + 1}) > div:nth-child(1) > span:nth-child(4) > span:nth-child(2)").text
        except:
            med_price_dis = driverN.find_element(By.CSS_SELECTOR,
                                                 f"li.ais-InfiniteHits-item:nth-child({i + 1}) > div:nth-child(1) > span:nth-child(4) > span:nth-child(2)").text

        med_link = driverN.find_element(By.CSS_SELECTOR,
                                        f"li.ais-InfiniteHits-item:nth-child({i + 1}) > div:nth-child(1) > a:nth-child(1)").get_attribute(
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

    medicine_span_pharm = driverP.find_element(By.XPATH, "/html/body/div[1]/main/div/div/div/div[1]")
    medicines_name_pharm = medicine_span_pharm.find_elements(By.CLASS_NAME, "ProductCard_medicineName__8Ydfq")
    medicines_price_pharm = medicine_span_pharm.find_elements(By.CLASS_NAME, "ProductCard_ourPrice__yDytt")

    for i in range(2, len(medicines_name_pharm) + 2):
        # .LHS_container__mrQkM > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)
        med_lnks_pharm = driverP.find_element(By.CSS_SELECTOR,
                                              f".LHS_container__mrQkM > div:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
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

def getgovdist(StateName):
    StateName = str(StateName).upper()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)

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
    state.select_by_visible_text(StateName)
    time.sleep(1)

    districts_list = []
    dist_value = driver.find_element(By.XPATH, "//*[@id='Bppi_body_ddlDistrict']")
    district_webobject = Select(dist_value)
    
    for opt in district_webobject.options:
        districts_list.append(opt.text)
    
    driver.quit()
    return districts_list

def getgovmeds(statename, district_name):
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)

    weblink = "http://janaushadhi.gov.in/KendraDetails.aspx"
    driver.get(weblink)
    
    time.sleep(1)
    state_value = driver.find_element(By.XPATH, "//*[@id='Bppi_body_ddlState']")
    state = Select(state_value)
    
    time.sleep(1)
    state.select_by_visible_text(str(statename).upper())
    time.sleep(1)

    dist_value = driver.find_element(By.XPATH, "//*[@id='Bppi_body_ddlDistrict']")
    district = Select(dist_value)

    district.select_by_visible_text(str(district_name).upper())
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

def getgovproducts():
    FILE_PATH = os.path.join(BASE_DIR, 'application', 'govmeds.txt')
    with open(FILE_PATH, 'r') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    print(soup)
    medicines = soup.find('tbody')

    blank = []
    med_names = []
    for med_rows in medicines.find_all('tr'):
        heads = med_rows.find_all('td')
        for head in heads:
            med_names.append(head.text)
        blank.append(med_names)
        med_names = []
    print(blank)

    medicines = []
    for i in range(len(blank)):
        spare = {}
        name = blank[i][2]
        price = blank[i][4]
        price = '₹ ' + price
        category = blank[i][5]

        if price == "₹ Under Process":
            price = "Unavailable"

        spare.update({"SrNo": i+1, "MedName": name, "MedPrice": price, "Category": category})
        medicines.append(spare)

    num = random.randint(300, len(medicines))

    spare_meds = []

    for i in range(num):
        spare_meds.append(medicines[i])

    return spare_meds, len(spare_meds)

def mail(name,c_email,phone,subject,message,alt_meds):
    import smtplib
    from email.message import EmailMessage
    
    msg = EmailMessage()
    msg['Subject'] = 'Doctor test message'
    msg['From'] = 'karuneshtest16@gmail.com'
    msg['To'] = 'jyoti@somaiya.edu'
    body=f"Name: {name} \nEmail: {c_email} \nPhone: {phone}\nSubject: {subject}\nMessage: {message} \n\n Alternative Medicines: \n{alt_meds}"
    msg.set_content(body)

    
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp :
    
        smtp.login(user='karuneshtest16@gmail.com',password='npbi taxc bpkp xftc')
        smtp.send_message(msg)
