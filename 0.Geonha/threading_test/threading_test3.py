import sys
from threading import Thread
from builtins import super    # https://stackoverflow.com/a/30159479
import time

if sys.version_info >= (3, 0):
    _thread_target_key = '_target'
    _thread_args_key = '_args'
    _thread_kwargs_key = '_kwargs'
else:
    _thread_target_key = '_Thread__target'
    _thread_args_key = '_Thread__args'
    _thread_kwargs_key = '_Thread__kwargs'

class ThreadWithReturn(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None

    def run(self):
        target = getattr(self, _thread_target_key)
        if not target is None:
            self._return = target(
                *getattr(self, _thread_args_key),
                **getattr(self, _thread_kwargs_key)
            )

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self._return

# TEST TARGET FUNCTION
def giveMe(arg, seconds=None):
    if not seconds is None:
        time.sleep(seconds)
    return arg

# TEST 1
my_thread = ThreadWithReturn(target=giveMe, args=('stringy',))
my_thread.start()
returned = my_thread.join()
print(returned)
# TEST 2
my_thread = ThreadWithReturn(target=giveMe, args=(None,))
my_thread.start()
returned = my_thread.join()
print(returned)
# (returned is None)

# # TEST 3
# my_thread = ThreadWithReturn(target=giveMe, args=('stringy',), kwargs={'seconds': 5})
# my_thread.start()
# returned = my_thread.join(timeout=2)
# print(returned)
# (returned is None) # because join() timed out before giveMe() finished

# TEST 4
my_thread = ThreadWithReturn(target=giveMe, args=(None,), kwargs={'seconds': 2})
my_thread.start()
returned = my_thread.join(timeout=(5))

print(my_thread.is_alive())
if my_thread.is_alive():
    # returned is None because join() timed out
    # this also means that giveMe() is still running in the background
    # handle this based on your app's logic
    print(returned)
    pass
else:
    print("mythread finish")
    # join() is finished, and so is giveMe()
    # BUT we could also be in a race condition, so we need to update returned, just in case
    returned = my_thread.join()
    print(returned)
# (returned == 'stringy')
