import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

## Pulls site list from link_generator.py result and converts to list form
with open('links.txt') as f:
     site_list = [line.rstrip('\n') for line in f]

## Initialize Browser for Data Gathering
     
driver = webdriver.Firefox()

with open('skinclub_database.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    fields = ['case', 'cost', 'type', 'skin', 'rarity', 'wear', 'ST', 'price', 'min_val', 'max_val', 'odds', 'site', 'update']
    writer.writerow(['case', 'cost', 'type', 'skin', 'rarity', 'wear', 'ST', 'price', 'min_val', 'max_val', 'odds', 'site', 'update'])

    for site in site_list:

        ## Load site w/ delay to allow full load
        driver.get(site)
        time.sleep(3)

        ## Determine Case name & Cost
        case = driver.find_element(By.CLASS_NAME,'case-title').get_attribute('textContent')
        cost = driver.find_element(By.CLASS_NAME,'price').get_attribute('textContent')

        ## Last Updated Time
        raw_update = driver.find_element(By.CLASS_NAME,'title-check-odds-range').get_attribute('textContent')
        update = raw_update.split('updated ',1)[1]

        skin_list_element = driver.find_element(By.CLASS_NAME,'skins-list')
        skin_pool = skin_list_element.find_elements(By.CLASS_NAME,'case-skin')

        ## Locate Reward Tables
        for item in skin_pool:

            ## Type of Weapon & Skin Name
            type = item.find_element(By.CLASS_NAME,'case-skin__name').get_attribute('textContent')
            skin = item.find_element(By.CLASS_NAME,'case-skin__title').get_attribute('textContent')
            
            ## Rarity of Skin (TO-DO - Add Names instead of Numeric Value | Will do during munging)
            raw_rarity = item.get_attribute("class")
            str_rarity = raw_rarity.split('rarity-',1)[1]
            rarity = int(str_rarity)

            ## Isolate individual Reward
            variation = item.find_elements(By.CLASS_NAME,'pf-table-row')
            ind = 0

            ## Skip Header Row
            for diff in variation:
                if ind == 0:
                    ind = 1
                    pass
                else:
                ## Check Wear and Stattrak        
                    raw_wear = diff.find_element(By.CLASS_NAME,'quality')
                    wear = raw_wear.get_attribute('textContent')
                    raw_ST = raw_wear.get_attribute("class")
                    if raw_ST == "quality stattrak":
                        ST = 1
                    else:
                        ST = 0  
                ## Check Price
                    price = diff.find_element(By.CLASS_NAME,'price').get_attribute('textContent')

                ## Check Odds and Ranges
                    range_odds = diff.find_elements(By.CLASS_NAME,'table-cell')
                    val_1 = 0
                    for diff_2 in range_odds:
                        if val_1 == 0:
                            val_1 = 1
                            pass
                        elif val_1 == 1:
                            range = diff_2.get_attribute('textContent')
                            min_val = range.split(' - ')[0]
                            max_val = range.split(' - ')[1]
                            val_1 = 2
                        elif val_1 == 2:
                            odds = diff_2.get_attribute('textContent')

                        ## Print Each Retrived Object & write out data into .csv file
                            print(case, cost, type, skin, rarity, wear, ST, price, min_val, max_val, odds, site, update)
                            writer.writerow([case, cost, type, skin, rarity, wear, ST, price, min_val, max_val, odds, site, update])

## Close the Websriver
driver.quit()