from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# radio box will be added.

def place_num_crawl(year, month, web):

    # get to website
    options = Options()
    options.add_argument("--disable-notifications")
    
    chrome = webdriver.Chrome('data/chromedriver.exe', chrome_options=options)
    chrome.get(web)

    time.sleep(1)

    # choose year
    wait = WebDriverWait(chrome, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div/div[1]/div[1]/div/div/select[1]')))
    select_elementsY = chrome.find_elements(By.XPATH, '//*[@id="searchPanel"]/div/div[1]/div[1]/div/div/select[1]')

    ## Check the number of elements found
    if len(select_elementsY) > 0:
        ## select the first element from the list
        selectY = Select(select_elementsY[0])

        ## select year
        selectY.select_by_value(str(year))

    else:
        print(f"No matching {year}y found.")

    
    # choose month
    wait = WebDriverWait(chrome, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div/div[1]/div[1]/div/div/select[2]')))
    select_elementsM = chrome.find_elements(By.XPATH, '//*[@id="searchPanel"]/div/div[1]/div[1]/div/div/select[2]')

    ## Check the number of elements found
    if len(select_elementsM) > 0:
        ## select the first element from the list
        selectM = Select(select_elementsM[0])

        ## select month
        selectM.select_by_value(str(month))

    else:
        print(f"No matching {month}m found.")

    # choose Changhua
    ## locate dropdown and click
    wait = WebDriverWait(chrome, 10)
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchPanel"]/div/div[1]/div[2]/div/div/div/button')))
    dropdown.click()

    ## Locate checkbox and click
    checkbox_selector = f'input[type="checkbox"][value="10007000"]'
    Changhua = chrome.find_elements(By.CSS_SELECTOR, checkbox_selector)
    if Changhua:
        Changhua[0].click()
    else:
        print("Locate checkbox failed.")

    ## submit
    wait = WebDriverWait(chrome, 10)
    send = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchPanel"]/div/div[3]/div/button')))
    send.click()

    # scrape data
    wait = WebDriverWait(chrome, 10)
    table_locator = (By.XPATH, '//*[@id="datatable"]/tbody')
    wait.until(EC.visibility_of_element_located(table_locator))

    temp_data_li = []
    for page in range(1,7):
        place = chrome.find_elements(By.XPATH, '//*[@id="datatable"]/tbody/tr/td[1]')
        num = chrome.find_elements(By.XPATH, '//*[@id="datatable"]/tbody/tr/td[2]')

        ## Check if any elements were found
        if place and num:
            
            for i in range(0,5):
                data_dict = {}
                if page == 6 and i == 1:
                    break
                    
                place_text = place[i].text #02468 為行政區 13579為人數: (1/2) != int()
                num_text = num[i].text
                
                data_dict['place'] = place_text
                data_dict['num'] = num_text
                
                
                temp_data_li.append(data_dict)
        else:
            print(f"{year}.{month} no matching elements found.")
        

        link = chrome.find_elements(By.XPATH, '/html/body/section/div/section/div/div[3]/section/div/div/div[3]/div[2]/div/ul/li[7]/a')
        link[0].click()

    time.sleep(1)

    chrome.close()

    return temp_data_li
