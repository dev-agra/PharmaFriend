from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

chrome_driver_path = "C:\Programming\Development\chromedriver.exe"

op = webdriver.ChromeOptions()
op.add_argument('headless')

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=op)


def didyoumean(medname):
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


def func1():
    func1.x, func1.y = didyoumean("Nitrolong")


def func2():
    a = func1.x
    print(a)

func1()
func2()
