from selenium.common.exceptions import NoSuchElementException

# Following this approach: https://guicommits.com/handling-exceptions-in-python-like-a-pro/


class NoCardImageFoundException(NoSuchElementException):
    def __init__(self, card_id):
        self.card_id = card_id
        super().__init__(
            f"card id {card_id} exhibit problems when selenium try to retrieve card's image"
        )


class NoFeatureAvailableException(NoSuchElementException):
    def __init__(self, card_id, card_feature):
        self.card_id = card_id
        self.card_feature = card_feature
        super().__init__(
            f"It's not possible to find a feature for card {card_id} in the xpath {card_feature}"
        )


class ManaCostSymbolException(NoSuchElementException):
    def __init__(self, card_id):
        self.card_id = card_id
        super().__init__(
            f"card id {card_id} exhibit problems when selenium try to retrieve card's mana symbols"
        )


class NoCardTextAvailableException(NoSuchElementException):
    def __init__(self, card_id):
        self.card_id = card_id
        super().__init__(
            f"Card {card_id} doesn't have any card text available"
        )
