from bs4 import BeautifulSoup
import pandas as pd
import requests
from urllib.error import URLError

inp=input("enter your product:")
List =inp.split()
length=len(List)


BASEURL="https://www.jumia.ma/"
URL="https://www.jumia.ma/catalog/?q="

for l in range(0,length):
  URL+=f"{List[l]}+"


MyURL=URL[:-1]

Mylist=[]

page = 0

while True:

    page+=1

    PAGEurl = MyURL + f"&page={page}#catalog-listing"

    response=requests.get(PAGEurl)

    soup = BeautifulSoup(response.content, "lxml")

    next_page = soup.select_one('[aria-label="Page suivante"]')
    div = soup.find_all("article",class_="prd _fb col c-prd")
    for element in div:
        for h in  element.find_all("a",href=True):
            Mylist.append( BASEURL + h["href"])

    if next_page is None:
                break

namelist=[]
pricelist=[]


for link in Mylist:
  response=requests.get(link)
  soup= BeautifulSoup(response.content, "lxml")
  name=soup.find("h1",class_="-fs20 -pts -pbxs").text.strip()
  div=soup.find("div",class_="-hr -mtxs -pvs").text.strip()
  price= div.split(" ")[0]
  namelist.append(name)
  pricelist.append(price)



for i in range(len(pricelist)):
  if len(pricelist[i]) > 6:
    pricelist[i]=pricelist[i].replace(',', '')


pricelist =list(map(float, pricelist))
   
min_of_list =min(pricelist)
index = pricelist.index(min_of_list)

dic ={

 '   '     :pricelist,
 '  '      :namelist


 }

df = pd.DataFrame(dic)
pd.set_option('display.max_colwidth', None)
print(df)
print("\n")
print("the lower price is :")
print(str(df.loc[[index]]))
print("\n")