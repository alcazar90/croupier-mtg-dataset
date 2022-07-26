"""
    File: card_retriever.py

    The task of this file is to download card features (e.g. text, mana cost, power and toughness, and so on) and the
    card images from The Gatherer. There are configurations that can handle in gatherer_croupier/config.py such as
    the path directories and the name of the files.

    Please see the usage section on the README.
"""
import os
import ssl
import csv
import argparse
import pandas as pd
import logging
import coloredlogs
from urllib.request import urlretrieve

from gatherer_croupier.driver import initialize_driver
from gatherer_croupier.exceptions import NoCardImageFoundException, NoFeatureAvailableException, \
    ManaCostSymbolException, NoCardTextAvailableException
from gatherer_croupier.utils import get_card_text, get_xpath_text, get_mana_cost, get_img_information
from gatherer_croupier.config import XpathCardFeatures, CARD_DIRECTORY_PATH, CARD_IMAGE_PATH, \
    CARD_INFORMATION_PATH

# Initialize logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')

# Avoid certificate for download image
ssl._create_default_https_context = ssl._create_unverified_context

# Initialize the parser
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("creature_type", help="Enter the creature type")
group.add_argument("-i", "--card_id", help="Option to download a specific card using its id", type=int)
group.add_argument("-n", "--number", help="Specify the number of cards to download (randomly choice from dir)",
                   type=int)
args = parser.parse_args()

# TODO: check if the file card_database.csv exists in CARD_DIRECTORY_PATH exists. Otherwise, stop the program and
# return a message that a card_database is required first...


if __name__ == '__main__':

    # Open card_directory to get card's url
    cards = pd.read_csv(CARD_DIRECTORY_PATH)
    cards = cards.loc[cards.subtype == args.creature_type, :]
    # TODO: check creature if the creature type is available in the card_database.csv. Raise an exception if not

    if args.number:
        # If the option -n was specified in the command line
        cards = cards.sample(args.number, random_state=42)
    elif args.card_id:
        cards = cards.loc[cards.id == args.card_id, :]

    NUM_CARDS = cards.shape[0]
    logging.info(f"[START] There are {NUM_CARDS} {args.creature_type}'s cards to download its information...")

    # Check if the data/subtype exists, following config.py paths
    logger.info(f'[ACTION] Checking if directory {CARD_IMAGE_PATH}/{args.creature_type.lower()} exists')
    check_path = os.path.isdir(f"{CARD_IMAGE_PATH}/{args.creature_type.lower()}")
    if check_path:
        logger.info('[STATUS] Directory exists')
    else:
        logger.info(f"[STATUS] The {CARD_IMAGE_PATH}/{args.creature_type.lower()} directory will be create...")
        os.makedirs(f"{CARD_IMAGE_PATH}/{args.creature_type.lower()}")
    CARD_IMAGE_PATH += f"/{args.creature_type.lower()}"

    for i in range(NUM_CARDS):

        # Establish connection given the card information (from card_database.csv)
        # ---------------------------------------------------------------------------------------------------------------
        # TODO: check w.r.t something (log or file) if the information and image for the current_id it was downloaded

        current_id = cards.iloc[i, 0]
        logger.info(f'[PROGRESS] Iteration {i + 1}/{NUM_CARDS}, establish connection for card id {current_id}')
        driver = initialize_driver(headless=True, install=False)
        img_url = cards.iloc[i, 3]
        driver.get(img_url)
        logger.info('[STATUS] Connection successful')

        # Extract the image source and extension given the card url and xpath. Download & Save in a folder the image
        # ---------------------------------------------------------------------------------------------------------------

        try:
            img_src, img_ext = get_img_information(driver, XpathCardFeatures.IMAGE.value)
            logger.info(f'[STATUS] Image source (with {img_ext} extension) retrieved: {img_src}')
        except NoCardImageFoundException:
            logger.info(f'[Exception] Skip card {current_id} because doble page format')
            driver.quit()
            continue

        logger.info(f'[WRITE] Downloading the image of card {current_id} and storing in the folder '
                    f'{CARD_IMAGE_PATH}/{current_id}_{args.creature_type.lower()}')

        urlretrieve(img_src, f'{CARD_IMAGE_PATH}/{current_id}_{args.creature_type.lower()}.{img_ext}')

        # Extract card information and store into CARD_INFORMATION_PATH file
        # ---------------------------------------------------------------------------------------------------------------

        # List to append card information
        row_to_csv = [current_id]

        for feature in XpathCardFeatures:
            logger.info(f'[ACTION] Extracting the feature {feature.name}')
            if feature.name == 'MANA_COST_SYMBOL':
                try:
                    row_to_csv.append(get_mana_cost(driver, feature.value))
                except ManaCostSymbolException:
                    logger.info(f'[Exception] Problem extracting mana cost symbols for card {current_id}')
                    row_to_csv.append('')
            elif feature.name == 'CARD_TEXT':
                try:
                    row_to_csv.append(get_card_text(driver, feature.value))
                except NoCardTextAvailableException:
                    logger.info(f'[Exception] No card text available for card {current_id}')
                    row_to_csv.append('')
            else:
                try:
                    row_to_csv.append(get_xpath_text(driver, feature.value))
                except NoFeatureAvailableException:
                    logger.info(f'[Exception] No feature {feature.name} available for card {current_id}')
                    row_to_csv.append('')

        logger.info(f'[STATUS] Card features extraction successful!')
        logger.info(f'[WRITE] Append card features from card_id: {current_id} into card_information.csv')

        # Append the row_to_csv into the csv file with the extracted card information
        with open(CARD_INFORMATION_PATH, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row_to_csv)
        csvFile.close()

        # Quit connection (shut down the geckodriver not only close the tab like driver.close() does)
        # ---------------------------------------------------------------------------------------------------------------
        driver.quit()
