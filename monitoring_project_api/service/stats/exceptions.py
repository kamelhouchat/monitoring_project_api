"""Stats methods custom exceptions"""


class StatsException(Exception):
    """Stats base exception.

        Attributes:
            message -- explanation of the error
    """

    def __init__(self, message="Stats methods exception"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class AcceptedURLsException(StatsException):
    """Accepted URLs method exception"""

    def __init__(self, message="Accepted URLs method exception"):
        self.message = message
        super(AcceptedURLsException, self).__init__(message=message)


class BlackIPAddressException(StatsException):
    """Black ip address method exception"""

    def __init__(self, message="Black ip address method exception"):
        self.message = message
        super(BlackIPAddressException, self).__init__(message=message)
