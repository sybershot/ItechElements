import time


def waituntiltrue(timeout=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            while time.time() < start + timeout:
                if bool(func(*args, **kwargs)):
                    return True
                else:
                    continue
            return False
        return wrapper
    return decorator
