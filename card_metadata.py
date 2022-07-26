"""
    File: card_metadata.py

    Creating a card database that contains card creatures meta-information (card_id and URL) and storing in a file.
"""
import time
import re
import coloredlogs
import logging
import csv
import argparse
import os

import selenium.common.exceptions
from selenium.webdriver.common.by import By

from gatherer_croupier.driver import initialize_driver
from gatherer_croupier.utils import get_id_string
from gatherer_croupier.config import CARD_DIRECTORY_PATH

# Create logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


# Initialize the parser
parser = argparse.ArgumentParser()
parser.add_argument("creature_type", help="Enter the creature type")
args = parser.parse_args()

# Check if the file exists
check_path = os.path.isfile(CARD_DIRECTORY_PATH)
if check_path:
    logger.info('[STATUS] card_database.csv exists')
else:
    with open(CARD_DIRECTORY_PATH, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['id', 'type', 'subtype', 'url'])
    csvFile.close()
    logger.info('[STATUS] card_database.csv successfully created')

if __name__ == '__main__':
    # Initialize the browser object
    driver = initialize_driver(headless=True, install=False)

    # URL to go to. Include f-string sys.argv argument creature
    url = f'https://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&action=advanced&type=+["Creature"]&subtype=+["{args.creature_type}"]'

    # Opens the URL in the browser
    driver.get(url)
    logger.info("[STATUS] URL successfully open...")

    MAX_ID = 100

    logger.info("How many pages are from that type of card?")
    xpath_pages = "/html/body/form/div[5]/div/div[1]/div[2]/div/div[7]/div"

    try:
        num_pages = driver.find_element(By.XPATH, xpath_pages)
        num_pages = re.sub('>|<', '', re.findall(r'>\d+<', num_pages.get_attribute('innerHTML'))[-1])
    except selenium.common.exceptions.NoSuchElementException:
        num_pages = '1'

    logger.info(f"[START] There are {num_pages} pages from this type of card to download...")
    num_pages = int(num_pages)

    visit_card_ids = set()
    for p in range(num_pages):
        # We are currently on page 0, just get the page if p!=0
        if p != 0:
            logger.info(f"[ACTION] Change to the page {p + 1}")
            url = f'https://gatherer.wizards.com/Pages/Search/Default.aspx?page={p}&action=advanced&type=+["Creature"]&subtype=+["{args.creature_type}"]'
            driver.get(url)
            logger.info(f"[STATUS] URL from page {p + 1} successfully open...")
        for i in range(0, MAX_ID):
            logger.info(f"[ACTION] Extract element #{i} with class='cardTitle' from the current page")
            element_id = get_id_string(i)
            xpath_string = f'//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_listRepeater_ctl{element_id}_cardTitle"] '
            card_info = driver.find_elements(By.XPATH, xpath_string)

            # Get href from the element extracted
            card_url = ''.join([elem.get_attribute('href') for elem in card_info]).replace(',', '')
            if card_url == '':
                logger.info(f"[STATUS] There are no more cards in the page {p + 1}...")
                break
            logger.info(f'[STATUS] Url correctly extracted: {card_url}')
            logger.info(card_url)

            # Get card id from href
            card_id = re.findall(r'\d+', card_url)[0]

            # Check if the card_id was not explored
            logger.info(f"Check if card-id {card_id} was not explored...")
            if card_id in visit_card_ids:
                logger.info(f"The card-id {card_id} was already explored...skip this card!!")
                continue
            else:
                logger.info(f"[EXCEPTION] The card-id {card_id} was not explored, proceed to store info in the csv file")
                visit_card_ids.add(card_id)

            logger.info('[WRITE] Add the information on card_database.csv')

            with open(CARD_DIRECTORY_PATH, 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([card_id, "Creature", args.creature_type, card_url])
            csvFile.close()
            logger.info("[STATUS] Information correctly added...")

        # Close the browser
        logger.info(f"[STATUS] Page {p + 1} successfully scrapped")

        # Wait 1 seconds before go to the next page
        logger.info("[TIME] Wait one second before go to the next page...")
        time.sleep(1)
    logger.info("[STATUS] All info was scrapped successfully!")
    driver.quit()
