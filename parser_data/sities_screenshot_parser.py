import os
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# Parser parameters
options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148')
options.add_argument('--window-size=375,812')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

site_urls = pd.read_csv('./parser_data/top-1m.csv') # Change me

if not os.path.exists('./parser_data/screenshots'):
    os.makedirs('./parser_data/screenshots')

for idx, row in site_urls.iterrows():
    site_url = row.iloc[0]

    if not site_url.startswith('http'):
        site_url = 'https://' + site_url

    try:
        driver.get(site_url)
    except WebDriverException as e:
        traceback_info = str(e) 
        print(f"Access error to {site_url}: {traceback_info}")

    screenshot_name = f'screenshot_{site_url.replace("https://", "").replace(".", "_")}.png'
    driver.save_screenshot(os.path.join('./parser_data/screenshots', screenshot_name))
    
    print(f' The screenshot was done for page: {site_url} and save to file {screenshot_name}')

driver.quit()