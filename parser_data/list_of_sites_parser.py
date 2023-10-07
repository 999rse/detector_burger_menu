from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import pandas as pd
import os


url_website = 'https://www.liveinternet.ru/rating/#page=' # Change me

chrome_driver_path = './parser_data/driver/chromedriver'

service = Service(chrome_driver_path)

options = webdriver.ChromeOptions()
options.add_argument('--headless')

def selector_structure(link_element):
    """
    Return structure of selector

    :link_elemnet - Order number of the link we want to get
    """
    return f'body > section > div > section > section > div#rows > div:nth-child({link_element}) > div.result-link > div.text > a'

def list_os_sites_parser(url, pages_on_website:int, elements_on_page:int):
    """
    Return csv file with list of links

    :url - website url. (In this case after `#page=` in url will be add number of page

    :pages_on_website - total page count 

    :elements_on_page - total links on page
    """

    if not os.path.exists('./parser_data/links'):
        os.makedirs('./parser_data/links')

    links_list = []

    for page in range(1, pages_on_website + 1):
        driver = webdriver.Chrome(service=service, options=options)
        url_new = url + str(page) + ';'
        print(url_new)
        driver.get(url_new)

        for element in range(1, elements_on_page + 1):
            selector = selector_structure(element)
            links = driver.find_elements(By.CSS_SELECTOR, selector)

            for link in links:
                links_list.append(link.get_attribute('href'))
                print(link.get_attribute('href'), element)
        
        driver.quit()

        if page % 10 == 0:
            print(f'Links on {page} pages have been preserved to output_links_{page}.csv')
            links_df = pd.DataFrame(links_list)
            links_df.to_csv(f'./parser_data/links/output_links_{page}.csv', index=False)
            
    links_df = pd.DataFrame(links_list)
    links_df.to_csv('./parser_data/links/output_links_all.csv', index=False)
    print('All links are saved to output_links.csv')


list_os_sites_parser(url=url_website, pages_on_website=5150, elements_on_page=30)