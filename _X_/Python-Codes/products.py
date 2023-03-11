from bs4 import BeautifulSoup
import random
import requests


def getgovproducts():
    MEDS = "http://janaushadhi.gov.in/ProductList.aspx"

    req = requests.get(MEDS)
    soup = BeautifulSoup(req.text, 'html.parser')

    medicines = soup.find('table', class_='table table-striped table-bordered table-hover')

    blank = []
    for med_rows in medicines.find_all('tr'):
        heads = med_rows.find_all('th')
        for head in heads:
            med_names = head.text
            blank.append(med_names)

    split_data = [blank[x:x+5] for x in range(0, len(blank), 5)]

    medicines = []

    for i in range(len(split_data)):
        spare = {}
        name = split_data[i][2]
        price = split_data[i][4]

        if price == "Under Process":
            price = "Unavailable"

        spare.update({"Sr No.": i+1, "MedName": name, "MedPrice": price})
        medicines.append(spare)

    num = random.randint(300, len(medicines))

    spare_meds = []

    for i in range(num):
        spare_meds.append(medicines[i])

    return spare_meds


x = getgovproducts()

