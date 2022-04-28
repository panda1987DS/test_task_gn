"""Module for memorization
 the result of a function"""
from typing import Callable, Any
from collections import OrderedDict
from warnings import warn
import logging
import pickle

logger = logging.getLogger(__name__)
logging.basicConfig(filename="memoize_result.log", level=logging.DEBUG)


class Cache:
    def __init__(self, function: Callable[..., Any], maxsize: int, dump_memo: bool) -> Any:
        self.function = function
        self.maxsize = maxsize
        self.dump_memo = dump_memo
        self.path = f"{function.__name__}.pickle"
        if dump_memo:
            self.load()
        else:
            self.memo = OrderedDict()

    def __call__(self, *args, **kwargs):
        try:
            return self.memo[args]
        except KeyError:
            result = self.function(*args)
            self.memo[args] = result
            if self.dump_memo:
                self.dump()
            if not self.maxsize is None and len(self.memo) > self.maxsize:
                self.memo.popitem(False)
            return result
        except TypeError:
            warn("Results are not hashed. Can't work with unhashable type parameters.", RuntimeWarning)
            result = self.function(*args)
            return result

    def dump(self):
        with open(self.path, 'wb') as handle:
            pickle.dump(self.memo, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(f"Save file {self.path}")

    def load(self):
        try:
            with open(self.path, 'rb') as handle:
                self.memo = pickle.load(handle)
            logger.info(f"Load file {self.path}")
        except FileNotFoundError:
            self.memo = OrderedDict()
            logger.info(f"File {self.path} not found")

    def clean(self):
        self.memo = OrderedDict()
        if self.dump_memo:
            self.dump()

    def __len__(self):
        return len(self.memo)

    def print(self):
        print(
            f"function = {self.function.__name__} \n"
            f"memo = {self.memo} \n"
            f"dump memo = {self.dump_memo} \n"
            f"maxsize = {self.maxsize}")


def memorize_result(maxsize: int = None, dump_memo: bool = False):
    """Python decorator for memorization
      the result of a function
      :param maxsize: number of values to be remembered
      :param dump_memo: save to disk flag
      :return:
      """

    def memorize_result_(function):
        return Cache(function, maxsize, dump_memo)

    return memorize_result_
