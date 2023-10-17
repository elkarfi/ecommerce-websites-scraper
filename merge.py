from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.error import URLError
from collections import OrderedDict


inp = input("enter your product:")   # cz109ae
List = inp.split()
length = len(List)

BaseURL = "https://www.jumia.ma/"
FirstURL = "https://www.jumia.ma/catalog/?q="
SecondURL = "https://www.electroplanet.ma/recherche?q="


for l in range(0, length):
    FirstURL += f"{List[l]}+"
    SecondURL += f"{List[l]}+"


FirstMyURL = FirstURL[:-1]
SecondMyURL = SecondURL[:-1]

Myfirstlist = []
Mysecondlist = []

page = 0

while True:

    page += 1

    FirstPAGEurl = FirstMyURL + f"&page={page}#catalog-listing"
    SecondPAGEurl = SecondMyURL + f"&p={page}"

    r1 = requests.get(FirstPAGEurl)
    r2 = requests.get(SecondPAGEurl)

    soup1 = BeautifulSoup(r1.content, "lxml")
    soup2 = BeautifulSoup(r2.content, "lxml")

    next_page1 = soup1.select_one('[aria-label="Page suivante"]')
    next_page2 = soup2.select_one('[title="Voir plus"]')

    all1 = soup1.find_all("article", class_="prd _fb col c-prd")
    all2 = soup2.find_all(
        "li", class_="item product product-item col-lg-3 col-md-3 col-sm-4 col-xs-12")

    for element in all1:
        for h1 in element.find_all("a", href=True):
            Myfirstlist.append(BaseURL + h1["href"])

    for l in all2:
        for h2 in l.find_all("a", href=True):
            Mysecondlist.append(h2["href"])

    if next_page1 is None and next_page2 is None:
        break


Mysecondlist[:] = (
    value for value in Mysecondlist if value != "javascript:void(0)")



Myfirstlist = list(OrderedDict.fromkeys(Myfirstlist))
Mysecondlist = list(OrderedDict.fromkeys(Mysecondlist))


namelist = []
pricelist = []
_namelist = []
_pricelist = []
linnks=[]



c = 0

for link in Myfirstlist:
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "lxml")
    name = soup.find("h1", class_="-fs20 -pts -pbxs").text.strip()
    div = soup.find("div", class_="-hr -mtxs -pvs").text.strip()
    price = div.split(" ")[0]
    namelist.append(name)
    pricelist.append(price)

    # divv = soup.find("div", class_="sldr _img _prod -rad4 -oh -mbs")

    # links = divv.a["href"]
    # linnks.append(links)

    c += 1
    print(c)
    print(link)
    # print(links)



for _link in Mysecondlist:
    _response = requests.get(_link)
    _soup = BeautifulSoup(_response.content, "lxml")
    _name = _soup.find("span", class_="ref").text.strip()
    _price = _soup.find("span", class_="price").text.strip()
    _namelist.append(_name)
    _pricelist.append(_price)
    c += 1
    print(c)
    print(_link)


for i in range(len(pricelist)):
    if len(pricelist[i]) > 6:
        pricelist[i] = pricelist[i].replace(',', '')


pricelist = list(map(float, pricelist))
min_of_list = min(pricelist)
index = pricelist.index(min_of_list)


for j in range(len(_pricelist)):
    _pricelist[j] = _pricelist[j].replace(' ', '')

_pricelist = list(map(int, _pricelist))
_min_of_list = min(_pricelist,default=None)
index0 = _pricelist.index(_min_of_list)


print("\n")

print("lower price jumia:" ,min_of_list)
l_ink=linnks[index]
print(l_ink)
print("lower price electoplanet:",_min_of_list)





dic1 = {

    '  ': namelist,
    '   ': pricelist

}


dic2 = {


    '  ': _namelist,
    '   ': _pricelist


}

df1= pd.DataFrame(dic1)
df2= pd.DataFrame(dic2)


pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

print(df1)
print("\n")
print("the lower price is :")
print(df1.loc[[index][0]][1])

print("\n")
print("     -----------------------------------------")

print(df2)
print("\n")
print("the lower price is :")
print(df2.loc[[index][0]][1])
print("\n")




