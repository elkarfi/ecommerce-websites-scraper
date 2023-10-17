from bs4 import BeautifulSoup
import requests
import pandas as pd


inp = input("enter your product:")
List = inp.split()
length = len(List)


URL = "https://www.electroplanet.ma/recherche?q="

for l in range(0, length):
    URL += f"{List[l]}+"


MyURL = URL[:-1]

Mylist = []

page = 0

while True:

    page += 1

    PAGEurl = MyURL + f"&p={page}"
    r = requests.get(PAGEurl)
    soup = BeautifulSoup(r.content, "lxml")

    next_page = soup.select_one('[title="Voir plus"]')

    all = soup.find_all("li", class_="item product product-item col-lg-3 col-md-3 col-sm-4 col-xs-12")

    for l in all:
        for h in l.find_all("a", href=True):
            Mylist.append(h["href"])

    if next_page is None:
            break


Mylist[:] = (value for value in Mylist if value != "javascript:void(0)")

namelist=[]
pricelist=[]

for link in Mylist:
    response=requests.get(link)
    soup= BeautifulSoup(response.content, "lxml")
    name=soup.find("span",class_="ref").text.strip()
    price=soup.find("span",class_="price").text.strip()
    namelist.append(name)
    pricelist.append(price)



for i in range(len(pricelist)):
    pricelist[i]=pricelist[i].replace(' ', '')

pricelist =list(map(int, pricelist))
min_of_list =min(pricelist)

index = pricelist.index(min_of_list)

dic ={

 '   '     :pricelist,
 '  '      :namelist


 }

df = pd.DataFrame(dic)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print(df)
print("\n")
print("the lower price is :")
print(df.loc[[index]])
print("\n")