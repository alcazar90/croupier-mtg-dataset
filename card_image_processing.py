"""
    Problem with opencv-python and PyCharm: https://github.com/opencv/opencv/issues/20997
"""
import cv2 as cv
import os
from pathlib import Path
from gatherer_croupier.config import CARD_IMAGE_PATH
from gatherer_croupier.utils import crop_image

import logging
import coloredlogs

# Init Path object
CARD_IMAGE_PATH = Path(CARD_IMAGE_PATH)

# Listing subdirectories (aka creature types folders)
sub_dir = [x for x in CARD_IMAGE_PATH.iterdir() if x.is_dir()]

# Initialize logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')

# Create a dictionary with different proportions by each size tuple
PROP_SIZE = {
    (223, 310): (0.12, 0.9, 0.115, 0.54),
    (265, 370): (0.08, 0.92, 0.115, 0.555),
    (223, 311): (0.078, 0.914, 0.115, 0.552),
    (266, 370): (0.08, 0.912, 0.116, 0.55),
    (222, 310): (0.09, 0.91, 0.12, 0.55),
    (226, 311): (0.12, 0.88, 0.11, 0.54)
}

# Check if the data/subtype exists, following config.py paths
logger.info(f'[ACTION] Checking if the directory {CARD_IMAGE_PATH.parent}/img_crop exists')
try:
    CARD_IMAGE_PATH.parent.joinpath('img_crop').mkdir(exist_ok=True)
    logger.info(f"[STATUS] The {CARD_IMAGE_PATH.parent}/img_crop directory will be created...")
except FileExistsError:
    logger.info('[STATUS] The directory currently exists, the content will be overwrite.')

SAVE_PATH = CARD_IMAGE_PATH.parent / 'img_crop'
logging.info(f'[ACTION] Save path set in: {SAVE_PATH}')

# Iterate through the subdirectories and crop each image, then save it into SAVE_PATH
counter = 1

for p in sub_dir:
    images = os.listdir(p)
    for img in images:
        path = p / img
        target = cv.imread(path.as_posix())
        target = crop_image(target, PROP_SIZE[target.shape[:2][::-1]])
        cv.imwrite(str(SAVE_PATH) + '/' + img, target)
        counter += 1

logger.info(f'[SUMMARY] {counter} cropped by the program')
