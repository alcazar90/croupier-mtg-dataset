"""
    Given the creatures cards in the directory "img/creature_type" the script creates a dataset structure using the
    following template and proportions 80%-10%-10%, respectively.

        - DATASET_PATH/train
        - DATASET_PATH/eval
        - DATASET_PATH/test

    The images will be cropped and shuffled into the 3 data subsets and organize by sub-folders with their corresponding
    labels, example:

        - DATASET_PATH/train
            - elf
            - goblin
            - knight
            - zombie

    For an example of the dataset structure, visit https://huggingface.co/datasets/alkzar90/croupier-mtg-dataset

   TODO: refactor the below code that uses pathlib using the pattern below based on page 67/Deep Learning for Coders.
   if not path.exists():
       path.exists():
           for o in creature_types:
               dest = (path/o)
               dest.mkdir(exist_ok=True)
               # 1. read and crop image
               # 2. save
"""
import cv2 as cv
import re
import os
import pandas as pd
import numpy as np
import logging
import coloredlogs

from pathlib import Path
from gatherer_croupier.config import CARD_IMAGE_PATH, CARD_DIRECTORY_PATH, DATASET_PATH
from gatherer_croupier.utils import crop_image


# Initialize logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')

CARD_IMAGE_PATH = Path(CARD_IMAGE_PATH)
sub_dir = [x for x in CARD_IMAGE_PATH.iterdir() if x.is_dir()]
labels = [p.parts[-1] for p in sub_dir]

# Create a dictionary with different proportions by each size tuple
PROP_SIZE = {
    (223, 310): (0.12, 0.9, 0.115, 0.54),
    (265, 370): (0.08, 0.92, 0.115, 0.555),
    (223, 311): (0.078, 0.914, 0.115, 0.552),
    (266, 370): (0.08, 0.912, 0.116, 0.55),
    (222, 310): (0.09, 0.91, 0.12, 0.55),
    (226, 311): (0.12, 0.88, 0.11, 0.54)
}


if __name__ == '__main__':

    # 0. Verify the HUGGING FACE DIR
    try:
        Path(DATASET_PATH).mkdir(exist_ok=True)
        Path(DATASET_PATH).joinpath('train').mkdir(exist_ok=True)
        Path(DATASET_PATH).joinpath('test').mkdir(exist_ok=True)
        Path(DATASET_PATH).joinpath('val').mkdir(exist_ok=True)
        for label in labels:
            Path(DATASET_PATH).joinpath('train').joinpath(label).mkdir(exist_ok=True)
            Path(DATASET_PATH).joinpath('test').joinpath(label).mkdir(exist_ok=True)
            Path(DATASET_PATH).joinpath('val').joinpath(label).mkdir(exist_ok=True)
    except FileExistsError:
        print('[STATUS] The directory currently exists, the content will be overwrite.')

    # 1. Create train, test, val set for checking which card_id belongs to what data split
    df = pd.read_csv(CARD_DIRECTORY_PATH, usecols=['id', 'subtype'])
    np.random.seed(42)
    df = df.iloc[np.random.permutation(len(df))]
    grouped_df = df.groupby('subtype')

    train_set = set()
    test_set = set()
    val_set = set()

    for label, data in grouped_df:
        train, test, val = np.split(data.id, [int(0.8 * len(data)), int(0.9 * len(data))])
        train_set = train_set.union(train.tolist())
        test_set = test_set.union(test.tolist())
        val_set = val_set.union(val.tolist())

    logger.info(f'Train set: {len(train_set)}')
    logger.info(f'Test set: {len(test_set)}')
    logger.info(f'Val set: {len(val_set)}')

    # 2. Iterate through...
    for path in sub_dir:
        images = os.listdir(path)
        for img in images:
            cur_path = path / img
            target = cv.imread(cur_path.as_posix())
            card_id = int(re.findall('^[0-9]+', img)[-1])
            label = re.findall('[a-z]+', img)[0]
            target = crop_image(target, PROP_SIZE[target.shape[:2][::-1]])
            if card_id in train_set:
                split = 'train'
            elif card_id in test_set:
                split = 'test'
            else:
                split = 'val'
            cv.imwrite(DATASET_PATH + '/' + split + '/' + label + '/' + img, target)
