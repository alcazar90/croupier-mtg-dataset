try:
    import context
except ModuleNotFoundError:
    import tests.context
from gatherer_croupier import driver
from gatherer_croupier.utils import get_img_information
from gatherer_croupier.config import XpathCardFeatures
from gatherer_croupier.exceptions import NoCardImageFoundException


import unittest


class TestDownloadImg(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = driver.initialize_driver(headless=True, install=False)

    def tearDown(self) -> None:
        self.driver.quit()

    def test_img_extension_png(self):
        """Test if the get_img_information() can handle correctly the img extension for a card with a PNG format"""
        CARD_URL_PNG = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=479441'
        self.driver.get(CARD_URL_PNG)
        img_src, img_ext = get_img_information(self.driver, XpathCardFeatures.IMAGE.value)
        return self.assertEqual('png', img_ext, 'Img extension incorrect, it should be "png"')

    def test_img_extension_jpeg(self):
        """Test if the get_img_information() can handle correctly the img extension for a card with a JPEG format"""
        CARD_URL_JPEG = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=146168'
        self.driver.get(CARD_URL_JPEG)
        img_src, img_ext = get_img_information(self.driver, XpathCardFeatures.IMAGE.value)
        return self.assertEqual('jpeg', img_ext, 'Img extension incorrect, it should be "jpeg"')

    def test_NoCardImageFoundException(self):
        """Test that NoCardImageFoundException raise correctly when get_img_information() is retrieving a card
        with double page website"""
        CARD_URL_DOBLE_PAGE = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=472967'
        self.driver.get(CARD_URL_DOBLE_PAGE)
        with self.assertRaises(NoCardImageFoundException):
            get_img_information(self.driver, XpathCardFeatures.IMAGE.value)

    def test_img_many_variations(self):
        """TODO: A card with 3 image variations"""
        CARD_URL_MANY_VAR = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=522242'
        pass

    def test_repeat_img(self):
        """TODO: A double card page with two different card but same image"""
        CARD_REPEAT_IMG = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=473061&part=Alter+Fate'
        CARD_REPEAT_IMG2 = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=472967'
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
