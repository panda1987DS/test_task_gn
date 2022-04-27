from functools import wraps, lru_cache
from collections import OrderedDict
from warnings import warn
import logging
import sys
import pickle

logger = logging.getLogger(__name__)
w_log = logging.FileHandler('memo.log')


def setup_logging():
    logging.basicConfig(
        stream=sys.stderr, level=logging.DEBUG,
    )


def memoize_result(maxsize: int = None, dump_memo: bool = False):
    def memoize_result_(function):
        if dump_memo:
            path = f"{function.__name__}.pickle"
            try:
                with open(path, 'rb') as handle:
                    memo = pickle.load(handle)
            except FileNotFoundError:
                memo = OrderedDict()
        else:
            memo = OrderedDict()

        @wraps(function)
        def wrapper(*args):
            print(memo)
            try:
                return memo[args]
            except KeyError:
                result = function(*args)
                memo[args] = result
                if dump_memo:
                    with open(path, 'wb') as handle:
                        pickle.dump(memo, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        logger.info(f"Save file {path}")
                if not maxsize is None and len(memo) > maxsize:
                    memo.popitem(False)
                return result
            except TypeError:
                warn("Results are not hashed. Can't work with unhashable type parameters. ", RuntimeWarning)
                result = function(*args)
                return result

        return wrapper

    return memoize_result_


@memoize_result(10, True)
def fibonacci(n, y):
    return n
    # if n < 2: return n
    # return fibonacci(n - 1) + fibonacci(n - 2)


@memoize_result(dump_memo=True)
def test_dict(d):
    return d * 3


def main():
    print(fibonacci(3, 7))
    print(fibonacci(2, 7))
    print(fibonacci(3, 7))
    logger.info("hello")
    # print(fibonacci(3, 2))
    test_dict(10)
    test_dict(10)
    # test_dict({1:2, 2:3})
    # test_dict({1:2, 2:3})


if __name__ == "__main__":
    main()
