class PricePageRetrievalError(Exception):
    pass


class UserInputError(Exception):
    pass


class AutomationPreventionError(PricePageRetrievalError):
    pass
