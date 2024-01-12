import pandas as pd
import os
from store_path import folder_path_2
from webcrawl_func import place_num_crawl


"""
Data range: 2010/1 ~ 2023/11

遷入、遷出、淨遷徙人數按性別分: "https://gis.ris.gov.tw/dashboard.html?key=E01&fbclid=IwAR0nInZHpHTonRuEr5OedtRx1QPkb4deF_HR6GYEl17nlfATd6n51LteEFk"
人口數按性別: 'https://gis.ris.gov.tw/dashboard.html?key=B01'
"""


url = 'https://gis.ris.gov.tw/dashboard.html?key=B01'

for month in range(4, 13):
    for y in range(2009, 2024):

        year = y - 1911 #ROC era
        data_li = place_num_crawl(year, month, url)
        print(data_li)
        df = pd.DataFrame(data_li, columns=['place', 'num'])

        if month < 10:
            file_name = f'{year}0{month}_彰化鄉鎮市.xlsx'
        else:
            file_name = f'{year}{month}_彰化鄉鎮市.xlsx'

        file_path = f'{folder_path_2}/{month}'
        full_path = os.path.join(file_path, file_name)
        df.to_excel(full_path, index = False, engine = 'openpyxl')
