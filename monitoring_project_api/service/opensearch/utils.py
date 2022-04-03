""""OpenSearch handler utils"""

import time
from functools import wraps
from logging import Logger
from typing import Callable
from typing import Type
from typing import Union


def retry(
        exception_to_check: Union[Type[Exception], tuple],
        *,
        tries: int = 5,
        delay: int = 1,
        backoff: int = 1,
        logger: Logger = None
) -> Callable:
    """
    Retry calling the decorated function using an exponential backoff.
    from: https://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    :param exception_to_check: the exception to check. may be a tuple of
    exceptions to check
    :type exception_to_check: Union[Type[Exception], tuple]
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
    each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: Logger
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            m_tries, m_delay = tries, delay
            while m_tries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), m_delay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(m_delay)
                    m_tries -= 1
                    m_delay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry
