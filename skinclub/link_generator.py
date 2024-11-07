import requests
from bs4 import BeautifulSoup

## Pull links from sitemap
sitemap = requests.get("https://skin.club/sitemap.xml")
alpha = BeautifulSoup(sitemap.content, "xml")
urls_from_xml = []
loc_tags = alpha.find_all('loc')
for loc in loc_tags:
    urls_from_xml.append(loc.get_text()) 

## Filter repeat links in different languages 
## Remove free cases and only link available cases
filtered_xml = []
for link in urls_from_xml:
    if '/en/cases/open' in link and 'lvl' not in link and 'free-case' not in link and 'premium-case' not in link and 'email-giveaway-case' not in link:
        filtered_xml.append(link)

## Write to file for shared info
with open('links.txt', 'w') as file:
    for l in filtered_xml:
        file.write(l+'\n')