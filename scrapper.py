"""
    Extract card information from the magic card database 'Gatherer'.
"""
import time
import sys
import re
import coloredlogs
import logging
import csv

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Create logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')

# Name of the columns to fill card_database.csv file
col = ['id', 'type', 'subtype', 'url']

# Get the creature type variable from the console
_, creature_type = sys.argv

# An utility function go get id's card in a string format
def get_id_string(id):
    """
    Given an int id of one or two digits, return the string id version always of length 2. Fill with a 0 at the left
    in case of the int was one of one digit.
    """
    id_str = str(id)
    if len(id_str) == 1:
        id_str = '0' + id_str
    return id_str

# Open connection to the card_database.csv file...
with open('card_database.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(col)

if __name__ == '__main__':
    # Initialize the browser object
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # URL to go to. Include f-string sys.argv argument creature
    url = f'https://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&action=advanced&type=+["Creature"]&subtype=+["{creature_type}"]'

    # Opens the URL in the browser
    driver.get(url)
    logger.info("URL successfully open...")

    MAX_ID=13

    logger.info("How many pages are from that type of card?")
    xpath_pages = "/html/body/form/div[5]/div/div[1]/div[2]/div/div[7]/div"

    try:
        num_pages = driver.find_element(By.XPATH, xpath_pages)
        num_pages = re.sub('>|<', '',re.findall(r'>\d+<', num_pages.get_attribute('innerHTML'))[-1])
    except selenium.common.exceptions.NoSuchElementException:
        num_pages = '1'

    logger.info(f"There are {num_pages} pages from this type of card to download...")
    num_pages = int(num_pages)

    visit_card_ids = set()
    for p in range(num_pages):
        # We are currently on page 0, just get the page if p!=0
        if p != 0:
            logger.info(f"Change to the page {p+1}")
            url = f'https://gatherer.wizards.com/Pages/Search/Default.aspx?page={p}&action=advanced&type=+["Creature"]&subtype=+["{creature_type}"]'
            driver.get(url)
            logger.info(f"URL from page {p+1} successfully open...")
        for i in range(0, MAX_ID):
            logger.info(f"Extract element #{i} with class='cardTitle' from the current page")
            element_id = get_id_string(i)
            xpath_string = f'//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_listRepeater_ctl{element_id}_cardTitle"]'
            card_info = driver.find_elements(By.XPATH, xpath_string)

            # Get href from the element extracted
            card_url = ''.join([elem.get_attribute('href') for elem in card_info]).replace(',', '')
            logger.info(f'Url correctly extracted: {card_url}')
            logger.info(card_url)

            # Get card id from href
            card_id = re.findall(r'\d+', card_url)[0]

            # Check if the card_id was not explored
            logger.info(f"Check if card-id {card_id} was not explored...")
            if card_id in visit_card_ids:
                logger.info(f"The card-id {card_id} was already explored...skip this card!!")
                next
            else:
                logger.info(f"The card-id {card_id} was not explored, proceed to store info in the csv file...")
                visit_card_ids.add(card_id)

            logger.info('Add the information on card_database.csv')

            with open('card_database.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([card_id, "Creature", creature_type, card_url])
            csvFile.close()
            logger.info("Information correctly added...")

        # Close the browser
        logger.info(f"Page {p+1} successfully scrapped")

        # Wait 1 seconds before go to the next page
        logger.info("Wait one second before go to the next page...")
        time.sleep(1)
    logger.info("All info was scrapped successfully!")
    driver.close()
