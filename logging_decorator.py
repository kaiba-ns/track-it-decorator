import functools
import logging


logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)s: %(message)s')


class TrackIt(object):
    """
    Logs out which decorated function (and its arguments) is about to be called as well as if that call was successful.
    It the error is raised, the decorator catches it, logs out on error and re-raises it.
    """

    def __init__(self, start=True, end=True):
        self.start = start
        self.end = end

    def __call__(self, fn, *args, **kwargs):
        @functools.wraps(fn)
        def wrapper_logger(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            if self.start:
                logging.info('Calling function {func} with following arguments: {arguments}'.format(func=fn.__name__, arguments=signature))
            try:
                value = fn(*args, **kwargs)
                if self.end:
                    logging.info('Called function {func} with following return value: {value}'.format(func=fn.__name__, value=value))
                return value
            except BaseException:
                logging.error('Unsuccessfully called function: Exception was raised')
                raise
        return wrapper_logger
