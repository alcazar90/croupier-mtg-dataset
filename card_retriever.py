"""
    card_retriever.py
    Script to retrieve information and download card image from card's url.
"""
import os
import logging
import coloredlogs
import ssl
import pandas as pd
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Define path constants (there could be a file with all the path constants)
# TODO: Move all constants into a module
CARD_DIRECTORY_PATH = './data/card_database.csv'
CARD_IMAGE_PATH = './data/img'
FILTER = 'Goblin'

# Create logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')

# Apparently this is not the BEST way to do this...instead update certificates
# https://stackoverflow.com/questions/43204012/how-to-disable-ssl-verification-for-urlretrieve
ssl._create_default_https_context = ssl._create_unverified_context

# Read csv with card's url
cards = pd.read_csv(CARD_DIRECTORY_PATH)
card_index = cards.loc[cards.subtype == FILTER, 'id']\
    .sample(5, random_state=42)\
    .index
cards = cards.iloc[card_index]
logger.info(cards)


# Check if the data/subtype exists
logger.info(f'Checking if directory {CARD_IMAGE_PATH}/{FILTER.lower()} exists')
check_path = os.path.isdir(f'{CARD_IMAGE_PATH}/{FILTER.lower()}"')
if ~check_path:
    os.makedirs(f'{CARD_IMAGE_PATH}/{FILTER.lower()}')
    logger.info(f'The {CARD_IMAGE_PATH}/{FILTER.lower()} directory will be create...')
else:
    logger.info('Directory exists')
CARD_IMAGE_PATH += f'/{FILTER.lower()}'

# Settings for init url-connection and iterate...
NUM_CARDS = cards.shape[0]
options = Options()
options.add_argument("--headless")

if __name__ == '__main__':
    for i in range(NUM_CARDS):
        # Establish connection given the card information (from card_database.csv)
        #---------------------------------------------------------------------------------------------------------------
        # TODO: check w.r.t something (log or file) if the information and image for the current_id it was downloaded
        current_id = cards.iloc[i, 0]
        logger.info('Establish connection...')
        driver = webdriver.Firefox(options=options)
        img_url = cards.iloc[i, 3]
        driver.get(img_url)
        logger.info('Connection successful')
        #text_xpath = "/html/body/form/div[5]/div/div[1]/div[2]/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div[2]/div[5]/div[2]/div[1]"

        # Extract img url given the XPATH and then extracting the 'src' attribute
        #---------------------------------------------------------------------------------------------------------------
        # TODO: exception to handle pages with two images
        # example: https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=472967
        img_xpath = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage"]'
        img = driver.find_element(By.XPATH, img_xpath)
        src = img.get_attribute('src')
        logger.info(src)
        logger.info(f'Img source retrieved: {img}')

        # Download the image and save in a folder
        #---------------------------------------------------------------------------------------------------------------
        logger.info('Downloading the image and storing in the folder...')
        urlretrieve(src, f'{CARD_IMAGE_PATH}/{current_id}_{FILTER.lower()}.jpeg')

        # Close connection
        #---------------------------------------------------------------------------------------------------------------
        driver.close()