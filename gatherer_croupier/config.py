import enum

CARD_DIRECTORY_PATH = './sample_data/card_database.csv'
CARD_INFORMATION_PATH = './sample_data/card_information.csv'
CARD_IMAGE_PATH = './sample_data/img'


class XpathCardFeatures(enum.Enum):
    CARD_NAME = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow"]/div[@class="value"]'
    MANA_COST_SYMBOL = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow"]/div[@class="value"]/img'
    MANA_COST_CONVERTED = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow"]/div[@class="value"]'
    TYPES = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow"]/div[@class="value"]'
    CARD_TEXT = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow"]/div[@class="value"]/div[' \
                '@class="cardtextbox"] '
    FLAVOR_TEXT = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_FlavorText"]/div[' \
                  '@class="flavortextbox"] '
    POWER_TOUGHNESS = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"]/div[@class="value"]'
    EXPANSION = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol"]'
    RARITY = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow"]/div[@class="value"]'
    CARD_NUMBER = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_CardNumberValue"]'
    ARTIST = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ArtistCredit"]'
    COMMUNITY_RATING = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_starRating"]'
    IMAGE = '//*[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage"]'


class XpathCreaturesTypes(enum.Enum):
    """Information to obtain all creatures type available"""
    # TODO: Download and use this information to check against the inputs receive by the parser
    CARD_URL = 'https://gatherer.wizards.com/Pages/Advanced.aspx'
    CREATURES_TYPES = '//*[@id="autoCompleteSourceBoxsubtypeAddText4_InnerTextBoxcontainer"]'

