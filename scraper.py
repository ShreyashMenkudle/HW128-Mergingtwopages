from selenium import webdriver 
from bs4 import BeautifulSoup 
import time 
import csv
import pandas as pd
import requests

headers = ["V_Mag", "Proper_name", "Bayer_designation", "Distance", "Spectral_class","Mass","Radius","Luminosity"] 
star_data = []
final_star_data = []
temp_list = [] 
new_star_data = []

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars" 
browser = webdriver.Chrome("chromedriver.exe") 
browser.get(START_URL) 
time.sleep(10)



def scrape(): 

    for i in range(0, 491):

        soup = BeautifulSoup(browser.page_source, "html.parser")
        star_table = soup.find('table')

    table_rows = star_table.find_all('tr') 
    
            
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text.rstrip() for i in td]
        temp_list.append(row)

Star_names = []
Distance =[]
Mass = []
Radius =[]
Lum = []

for i in range(1,len(temp_list)):
    Star_names.append(temp_list[i][1])
    Distance.append(temp_list[i][3])
    Mass.append(temp_list[i][5])
    Radius.append(temp_list[i][6])
    Lum.append(temp_list[i][7])

    df2 = pd.DataFrame(list(zip(Star_names,Distance,Mass,Radius,Lum)),columns=['Star_name','Distance','Mass','Radius','Luminosity'])
    print(df2)

    df2.to_csv('bright_stars.csv')
    print(f"{i} page done 1")


def scrape_more_data(hyperlink):
    try: 
        page = requests.get(hyperlink) 
        soup = BeautifulSoup(page.content, "html.parser") 
        temp_list = []

    
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}): 
            td_tags = tr_tag.find_all("td") 
            
            for td_tag in td_tags: 
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0]) 
                    
                except: 
                    temp_list.append("") 

        new_star_data.append(temp_list)

    except: 
        time.sleep(1) 
        scrape_more_data(hyperlink)

scrape()

for index, data in enumerate(star_data): 
    scrape_more_data(data[5]) 
    print(f"{index+1} page done 2") 

for index, data in enumerate(star_data): 
    new_star_data_element = new_star_data[index] 
    new_star_data_element = [elem.replace("\n", "") for elem in new_star_data_element] 
    new_star_data_element = new_star_data_element[:7] 
    final_star_data.append(data + new_star_data_element) 
    
with open("final.csv", "w") as f: 
    csvwriter = csv.writer(f) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(final_star_data)