from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from gatherer_croupier.exceptions import NoCardImageFoundException, NoFeatureAvailableException, \
    ManaCostSymbolException, NoCardTextAvailableException
from urllib.request import urlopen
import ssl
import re

# Apparently this is not the BEST way to do this...instead update certificates
# https://stackoverflow.com/questions/43204012/how-to-disable-ssl-verification-for-urlretrieve
ssl._create_default_https_context = ssl._create_unverified_context


def get_xpath_text(con, xpath):
    """Given a connection (con), extract the text on the web-element specified by the given xpath"""
    try:
        return con.find_element(By.XPATH, xpath).text
    except NoSuchElementException as ex:
        card_id = re.search("\\d+$", con.current_url)[0]
        raise NoFeatureAvailableException(card_id, xpath) from ex


def get_mana_cost(con, xpath):
    """Given a connection (con), extract the mana cost from alt elements' alt attribute by the specified xpath"""
    try:
        elements = con.find_elements(By.XPATH, xpath)
        return '-'.join([e.get_attribute('alt') for e in elements])
    except NoSuchElementException as ex:
        card_id = re.search("\\d+$", con.current_url)[0]
        raise ManaCostSymbolException(card_id) from ex


def get_card_text(con, xpath):
    """Given a connection (con), extract the card text checking if there is a skill that used mana cost to store it"""
    elements = con.find_elements(By.XPATH, xpath)
    if len(elements) == 0:
        # find_elements() return an empty list if it doesn't find anything with the given xpath
        card_id = re.search("\\d+$", con.current_url)[0]
        raise NoCardTextAvailableException(card_id)
    if len(elements) > 1:
        # 2-paragraphs scenario
        card_text = ''
        for elem in elements:
            card_text += elem.text
            check_img = elem.find_elements(By.XPATH, xpath + f'[{elements.index(elem) + 1}]' + '/img')
            if check_img:
                ability_cost = '-'.join([img.get_attribute('alt') for img in check_img])
                card_text = card_text + '[' + ability_cost + ']'
            card_text += '\n'
        return card_text
    else:
        # 1-paragraph scenario
        check_img = elements[0].find_elements(By.XPATH, xpath + '/img')
        ability_cost = '-'.join([img.get_attribute('alt') for img in check_img])
        if ability_cost:
            return elements[0].text + '[' + ability_cost + ']'
        else:
            return elements[0].text


def get_id_string(card_id):
    """Given an int id of one or two digits, return the string id version always of length 2. Fill with a 0 at the left
    in case of the int was one of one digit.
    """
    id_str = str(card_id)
    if len(id_str) == 1:
        id_str = '0' + id_str
    return id_str


def get_img_information(con, xpath):
    """Given a connection (con), extract the image information (img_src, img_ext) by the specified xpath. Return a
    tuple with image source and image extension strings (i.e. png, jpeg)"""
    try:
        img = con.find_element(By.XPATH, xpath)
        img_src = img.get_attribute('src')
    except NoSuchElementException as ex:
        # Obtain the card id for report in the message
        card_id = re.search("\\d+$", con.current_url)[0]
        # Trigger the custom exception NoCardImageFoundException defined in exceptions.py
        raise NoCardImageFoundException(card_id) from ex
    check_extension = urlopen(img_src) \
        .read() \
        .decode('utf-8', errors='ignore')
    if re.match("PNG", check_extension):
        return img_src, 'png'
    else:
        return img_src, 'jpeg'


def crop_image(image, props=(0.06, 0.94, 0.1, 0.57)):
    """Crop the image given the proportions in the X's and Y's dimensions"""
    WL, WR, HT, HB = props
    Y, X, _ = image.shape
    return image[int(Y * HT):int(Y * HB), int(X * WL):int(X * WR), :]

