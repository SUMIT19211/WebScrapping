import requests
from bs4 import BeautifulSoup
import pandas

r = requests.get("http://pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",
                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})


c = r.content
soup = BeautifulSoup(c, "html.parser")
# print(soup.prettify())

all = soup.find_all("div", {"class": "propertyRow"})

# print(all)

# print(len(all))
t = all[0].find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ", "")

page_no= soup.find_all("a",{"class":"Page"})[-1].text
print(page_no)

# print(t)

l = []
base_url = "http://pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s="
for page in range(0,int(page_no)*10,10):
    print(base_url+str(page)+".html")
    r = requests.get(base_url+str(page),headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c= r.content
    soup=BeautifulSoup(c,"html.parser")
    #print(soup.prettify())
    all = soup.find_all("div", {"class": "propertyRow"})
    for item in all:
        d={}

        d['Address'] = item.find_all("span", {"class": "propAddressCollapse"})[0].text
        d['Locality'] = item.find_all("span", {"class": "propAddressCollapse"})[1].text
        d['Price'] = item.find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ", "")
        try:
            d['Beds'] = item.find("span", {"class", "infoBed"}).text
        except:
            d['Beds'] = None
            # print("Beds information not available")
        try:
            d['Area'] = item.find("span", {"class", "infoSqFt"}).text
        except:
            d['Area'] = None
            # print("Information not available")
        try:
            d['Full Baths'] = item.find("span", {"class", "infoValueFullBath"}).text
        except:
            d['Full Baths'] = None
            # print("Information not available")

        for column in item.find_all("div", {"class": "columnGroup"}):
            # print(column)
            for feature_group, feature_name in zip(column.find_all("span", {"class": "featureGroup"}),column.find_all("span", {"class": "featureName"})):
                #print(feature_group.text, feature_name.text)
                if "Lot Size" in feature_group.text:
                    d['Lot Size'] = feature_name.text

        l.append(d)

df = pandas.DataFrame(l)
df.to_csv("Output.csv")
#print(df)

print(l)
