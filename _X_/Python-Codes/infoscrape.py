from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"


# Function to get all medicine info from ONEMG
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

        medinfo.update({"medname": medname, "medimg": src, "medinfo": medicine_info, "medpricedis": medpricedis,
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
        print(medicine_info)
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
                            alternatives_save = f'pay {alternatives_save}% less per Tablet'

                alternative_dict.update({"medname": alternatives_medname, "medmanuf": alternatives_pharma,
                                         "medprice": alternatives_price, "medsave": alternatives_save,
                                         "medtablets": alternatives_tablets,
                                         "medlink": alternatives_link})
                medicine_alternatives.append(alternative_dict)

        elif flag == 1:
            medicine_alternatives = ["Not Available"]

        medinfo.update({"medname": medname, "medimg": src, "medinfo": medicine_info, "medprice-dis": medicine_price_dis,
                        "medprice-mrp": medicine_price_mrp, "meduses": medicine_uses,
                        "medeffects-para": medicine_effect_info, "medeffects-list": medicine_side_effects,
                        "medmech": medicine_mechanism, "medsafety": medicine_safety, "medalt": medicine_alternatives})

    driver.quit()
    return medinfo


x = getinfo_onemg("https://www.1mg.com/drugs/rantac-150-tablet-30363")
print(x)
