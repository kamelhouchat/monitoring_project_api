"""Scheduler exception"""


class JobError(Exception):
    """Exception raised when error occurred during doing a job"""

    def __init__(self, message="Unknown error"):
        """
        Class initiator
        :param message: Explanation of the error
        """
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
