"""Detector custom exceptions"""


class DetectorException(Exception):
    """Detector base exception.

        Attributes:
            message -- explanation of the error
    """

    def __init__(self, message="Detector exception"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class InvalidWorkflowInputException(DetectorException):
    """Invalid workflow input exception"""

    def __init__(self, /, feature, *, message="Invalid workflow exception"):
        self.message = f'{message} -> {feature}'
        super(InvalidWorkflowInputException, self).__init__(message=message)


class InvalidDataSourceException(DetectorException):
    """Invalid data source exception"""

    def __init__(self, message="Invalid data source exception"):
        self.message = message
        super(InvalidDataSourceException, self).__init__(message=message)


class NoProcessingMethodFoundException(DetectorException):
    """No processing method found exception"""

    def __init__(self, message="No processing method found"):
        self.message = message
        super(NoProcessingMethodFoundException, self).__init__(message=message)
