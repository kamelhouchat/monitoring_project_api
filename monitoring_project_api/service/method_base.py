"""Detection Methods base class"""

import abc


class DetectionMethod(abc.ABC):

    @abc.abstractmethod
    def launch(self):
        """
        All detection methods must contain the method that allows to start
        the processing.
        """
        pass
