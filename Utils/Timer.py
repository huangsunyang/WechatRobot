import time


class Timer:
    def __init__(self):
        self.time = time.time()
        self.end_time = {}

    def update_time(self):
        self.time = time.time()
        for func, end_time in self.end_time:
            if time.time() >= end_time:
                func.join()

    def run_most(self, seconds):
        def decorator(func):
            def ret_func(*args, **kwargs):
                self.end_time[func] = time.time() + seconds
                ret = func(args, kwargs)
                del self.end_time[func]
                return ret
            return ret_func()
        return decorator


time_manager = Timer()
