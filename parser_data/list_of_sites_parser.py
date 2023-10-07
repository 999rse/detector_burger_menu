from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd
import os


url_website = 'https://www.liveinternet.ru/rating/#page='

options = webdriver.ChromeOptions()
options.add_argument('--headless')

def selector_structure(link_element):
    return f'body > section > div > section > section > div#rows > div:nth-child({link_element}) > div.result-link > div.text > a'

def list_os_sites_parser(url, pages_on_website:int, elements_on_page:int, attribute:str):

    if not os.path.exists('parser_data/links'):
        os.makedirs('parser_data/links')

    links_list = []

    for page in range(1, pages_on_website + 1):
        driver = webdriver.Chrome(options)
        url_new = url + str(page) + ';'
        print(url_new)
        driver.get(url_new)

        for element in range(1, elements_on_page + 1):
            selector = selector_structure(element)
            links = driver.find_elements(By.CSS_SELECTOR, selector)

            for link in links:
                links_list.append(link.get_attribute(attribute))
                print(link.get_attribute(attribute), element)
        
        driver.quit()

        if page % 10 == 0:
            print(f'Links on {page} pages have been preserved to output_links_{page}.csv')
            links_df = pd.DataFrame(links_list)
            links_df.to_csv(f'parser_data/links/output_links_{page}.csv', index=False)
            
    
    print('All links are saved to output_links.csv')
    links_df = pd.DataFrame(links_list)
    links_df.to_csv('parser_data/links/output_links_all.csv', index=False)


list_os_sites_parser(url=url_website, pages_on_website=5150, elements_on_page=30, attribute='href')