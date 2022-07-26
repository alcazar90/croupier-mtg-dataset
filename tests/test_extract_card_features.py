try:
    import context
except ModuleNotFoundError:
    import tests.context
from gatherer_croupier import driver
from gatherer_croupier.config import XpathCardFeatures
from gatherer_croupier.utils import get_xpath_text, get_mana_cost, get_card_text
from gatherer_croupier.exceptions import NoFeatureAvailableException, NoCardTextAvailableException

import unittest


class TestCardFeatures(unittest.TestCase):
    """Test suite for testing XpathCardFeatures enum (config.py) that contains the xpath to extract the card features
    together with the functions: get_xpath_text(), get_mana_cost(), and get_card_text()
    """

    def setUp(self) -> None:
        self.EXAMPLE_CARD_PATH = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=489559'
        self.driver = driver.initialize_driver(headless=True, install=False)
        self.driver.get(self.EXAMPLE_CARD_PATH)

    def tearDown(self) -> None:
        self.driver.quit()

    def test_card_name(self):
        """Extract the feature card name using XpathCardFeatures.CARD_NAME.value"""
        self.assertEqual('Volley Veteran', get_xpath_text(self.driver, XpathCardFeatures.CARD_NAME.value),
                         'Card name is incorrect, it should be "Volley Veteran"')

    def test_mana_cost(self):
        """Extract the feature mana cost with symbols include (e.g. mountains, swamps) using
        XpathCardFeatures.MANA_COST_SYMBOL.value"""
        self.assertEqual('3-Red', get_mana_cost(self.driver, XpathCardFeatures.MANA_COST_SYMBOL.value),
                         'Mana cost is not equal, it should be "3-Red"')

    def test_mana_cost_converted(self):
        """Extract the feature mana cost converted (i.e. total mana without consider different type lands) using
        XpathCardFeatures.MANA_COST_CONVERTED.value"""
        self.assertEqual('4', get_xpath_text(self.driver, XpathCardFeatures.MANA_COST_CONVERTED.value),
                         'Mana cost is not equal, it should be 4')

    def test_types(self):
        """Extract the feature types (e.g. Creature -- Goblin Warrior) using XpathCardFeatures.TYPES.value"""
        self.assertEqual('Creature — Goblin Warrior', get_xpath_text(self.driver, XpathCardFeatures.TYPES.value),
                         'Type creature is not equal, it should be "Creature — Goblin Warrior"')

    def test_card_text(self):
        """Extract the feature card text (i.e. text with card abilities) using XpathCardFeatures.CARD_TEXT.value"""
        self.assertEqual(
            'When Volley Veteran enters the battlefield, it deals damage to target creature an opponent controls equal '
            'to the number of Goblins you control.',
            get_card_text(self.driver, XpathCardFeatures.CARD_TEXT.value),
            'Card text is not equal!')

    def test_flavor_text(self):
        """Extract the feature flavor text (i.e. decorator text) using XpathCardFeatures.FLAVOR_TEXT.value"""
        self.assertEqual('"Fill the sky with stuff!"', get_xpath_text(self.driver, XpathCardFeatures.FLAVOR_TEXT.value),
                         'Flavor text is not equal, it should be said: "Fill the sky with stuff!"')

    def test_pt(self):
        """Extract the feature power and toughness using XpathCardFeatures.POWER_TOUGHNESS.value"""
        self.assertEqual('4 / 2', get_xpath_text(self.driver, XpathCardFeatures.POWER_TOUGHNESS.value),
                         'The Power/Toughness are not equals, it should be: 4 / 2')

    def test_expansion(self):
        """Extract the feature card expansion using XpathCardFeatures.EXPANSION.value"""
        self.assertEqual('Jumpstart', get_xpath_text(self.driver, XpathCardFeatures.EXPANSION.value),
                         'The expansion is not equal, it should be: "Jumpstart"')

    def test_rarity(self):
        """Extract the feature card rarity (e.g. 'Uncommon', 'Rare) using XpathCardFeatures.RARITY.value"""
        self.assertEqual('Uncommon', get_xpath_text(self.driver, XpathCardFeatures.RARITY.value),
                         'The rarity is not equal, it should be "Uncommon"')

    def test_card_number(self):
        """Extract the feature card number (from a given expansion collection) using
        XpathCardFeatures.CARD_NUMBER.value"""
        self.assertEqual('369', get_xpath_text(self.driver, XpathCardFeatures.CARD_NUMBER.value),
                         'The card number is not equal, it should be 369')

    def test_artist(self):
        """Extract the feature artist (who draw the card image) using XpathCardFeatures.ARTIST.value"""
        self.assertEqual('Craig J Spearing', get_xpath_text(self.driver, XpathCardFeatures.ARTIST.value),
                         'The artist name is not equal, it should be "Craig J Spearing"')


class TestCardText(unittest.TestCase):
    """Test suite for testing the function get_card_text() and how its handle different text cases structures"""

    def setUp(self) -> None:
        self.driver = driver.initialize_driver(headless=True, install=False)

    def tearDown(self) -> None:
        self.driver.quit()

    def test_one_paragraph(self):
        """A card with one paragraph without any ability that involved mana cost (symbol extraction)"""
        self.EXAMPLE_ONE_PARAGRAPH = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=442145'
        self.driver.get(self.EXAMPLE_ONE_PARAGRAPH)
        self.assertEqual(
            "Whenever you cast an instant or sorcery spell that targets only Zada, Hedron Grinder, copy that"
            " spell for each other creature you control that the spell could target. Each copy targets a"
            " different one of those creatures.",
            get_card_text(self.driver, XpathCardFeatures.CARD_TEXT.value),
            'Both texts are not equals')

    def test_multiple_paragraphs(self):
        """A card with two paragraphs without any ability that involved mana cost (symbol extraction)"""
        self.EXAMPLE_MANY_PARAGRAPHS = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=574235'
        self.driver.get(self.EXAMPLE_MANY_PARAGRAPHS)
        self.assertEqual('Flying, double team\nWhen Champions of Tyr enters the battlefield, you get a boon with "When'
                         ' you cast your next creature spell, that creature enters the battlefield with your choice of'
                         ' a +1/+1 counter, a flying counter, or a lifelink counter on it."\n',
                         get_card_text(self.driver, XpathCardFeatures.CARD_TEXT.value),
                         'Both texts are not equals')

    def test_text_with_cost_simple(self):
        """A card with one paragraph that includes an ability with mana cost"""
        self.EXAMPLE_COST_SIMPLE = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=146168'
        self.driver.get(self.EXAMPLE_COST_SIMPLE)
        self.assertEqual(', Sacrifice Boggart Forager: Target player shuffles their library.[Red]',
                         get_card_text(self.driver, XpathCardFeatures.CARD_TEXT.value),
                         'Both texts are not equals')

    def test_text_with_cost_complex1(self):
        """A card with two paragraphs and only the first one includes an ability with cost"""
        self.EXAMPLE_COST_COMPLEX1 = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=370530'
        self.driver.get(self.EXAMPLE_COST_COMPLEX1)
        self.assertEqual("Prowl (You may cast this for its prowl cost if you dealt combat damage to a player this turn"
                         " with a Goblin or Rogue.)[2-Black]\nWhen Earwig Squad enters the battlefield, if its prowl"
                         " cost was paid, search target opponent's library for three cards and exile them. Then that"
                         " player shuffles.\n",
                         get_card_text(self.driver, XpathCardFeatures.CARD_TEXT.value),
                         'Both texts are not equals')

    def test_text_with_cost_complex2(self):
        """A card with two paragraphs and only the second one includes an ability with cost"""
        self.EXAMPLE_COST_COMPLEX2 = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=489505'
        self.driver.get(self.EXAMPLE_COST_COMPLEX2)
        self.assertEqual("Haste\n, Sacrifice Fanatical Firebrand: It deals 1 damage to any target.[Tap]\n",
                         get_card_text(self.driver, XpathCardFeatures.CARD_TEXT.value),
                         'Both texts are not equals')

    def test_NoCardTextAvailableException(self):
        """A card without text (e.g. card token), the function should raise a NoCardTextAvailableException"""
        self.EXAMPLE_CARD_PATH = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=369082'
        self.driver.get(self.EXAMPLE_CARD_PATH)
        with self.assertRaises(NoCardTextAvailableException):
            get_card_text(self.driver, XpathCardFeatures.CARD_TEXT.value)

    def test_text_intricate_mana_between(self):
        """A card with an ability that generates 1 of 3 possible types of mana if you tap it"""
        # TODO: Improve mana generation/cost/ability extraction
        self.EXAMPLE_INTRICATE_MANA = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=522242'
        self.driver.get(self.EXAMPLE_INTRICATE_MANA)
        self.assertEqual("Exalted (Whenever a creature you control attacks alone, that creature gets +1/+1 until end of"
                         " turn.)\n: Add , , or .[Tap-Black-Red-Green]\n",
                         get_card_text(self.driver, XpathCardFeatures.CARD_TEXT.value),
                         'Both texts are not equals')


class TestNoFeatureAvailable(unittest.TestCase):
    """Test custom exception defined in the exceptions"""

    def setUp(self) -> None:
        self.driver = driver.initialize_driver(headless=True, install=False)

    def tearDown(self) -> None:
        self.driver.quit()

    def test_NoFeatureAvailableException(self):
        self.CARD_WITH_NO_FLAVOR_TEXT = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=2844'
        self.driver.get(self.CARD_WITH_NO_FLAVOR_TEXT)
        with self.assertRaises(NoFeatureAvailableException):
            get_xpath_text(self.driver, XpathCardFeatures.FLAVOR_TEXT.value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
