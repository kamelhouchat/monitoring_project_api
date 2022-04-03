"""Experta custom exceptions"""


class ExpertaException(Exception):
    """Experta base exception.

        Attributes:
            message -- explanation of the error
    """

    def __init__(self, message="Experta methods exception"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class ExpertaHelpersException(ExpertaException):
    """Experta helpers exception"""

    def __init__(self, message="Experta helpers exception"):
        self.message = message
        super(ExpertaHelpersException, self).__init__(message=message)
