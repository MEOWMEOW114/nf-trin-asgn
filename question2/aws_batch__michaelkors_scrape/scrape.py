import asyncio
"""
Set up the Necesarry imports for the script 
mainly selenium webdriver plugins necesarry to 
manipulate the chrome number. 
We also import pandas since we need to be able to 
clean and structure the data into csv once it
has been extracted.
""" 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import boto3
import os
from datetime import date
import time
from io import StringIO
from dotenv import load_dotenv
load_dotenv()
"""
Specify the Webdriver options 
"""
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized") # The Chrome window will open in full screen 
prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)
# options.add_argument("--headless") # The Chrome window will open in full screen 
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')


dest_s3_bucket = os.getenv('DEST_S3_BUCKET')
dest_aws_access_key_id = os.getenv('DEST_S3_ACCESS_KEY')
dest_aws_secret_access_key =  os.getenv('DEST_S3_SECRET_ACCESS_KEY')


async def main():
    TARGET = 'https://www.michaelkors.global/en_HK/women/handbags/_/N-1ysakls'
    company = 'michaelkors_global'
    category = 'woman/handbags'


    from selenium.webdriver.common.action_chains import ActionChains as AC
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(TARGET)
    driver.set_window_size(1600, 1024)

    # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
    SCROLL_PAUSE_TIME = 1.8
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(new_height, last_height)
        if new_height == last_height:
            break
        last_height = new_height

    print(last_height)
    # print(driver.page_source.encode("utf-8"))
    page_content = driver.page_source.encode("utf-8")

    
    today = date.today()
    date_string = today.strftime("%Y/%m/%d")
    s3_target = boto3.client('s3',aws_access_key_id=dest_aws_access_key_id, aws_secret_access_key=dest_aws_secret_access_key)
    
    key = f"raw/{date_string}/{company}/{category}/source.html"
    s3_target.put_object(Body=page_content, Bucket=dest_s3_bucket, Key=key)
    driver.quit()


if __name__ == '__main__':
    asyncio.run(main())  
