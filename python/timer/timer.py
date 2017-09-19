#coding=utf8
"""
timer

A small timer that support gevent or multi-threading.
Use get_timer to get a [Timer_class], which offers
start, cancel, acquire(threading), release(threading).
Use [Timer_class](delay, fn, *args, **kwargs) to get an
instance of Timer.
    delay - seconds before exceute
    fn - the function to be executed
    *args, **kwargs - args for the function
"""
import time
from threading import Lock,Timer
import gevent
import gevent.monkey
#please enable this in other modules
#gevent.monkey.patch_all(thread=False);

__all__ = ['get_timer',
           'test']

#获得timer类
def get_timer(ctype):
    """timer_class = get_timer(ctype), ctype must be 'threading' or 'gevent'"""
    if ctype == "threading":
        return _TimerT;
    elif ctype == "gevent":
        return _TimerM;
    else:
        return None;


class _Timer:
    """a basic timer """
    def start(self):
        pass

    def cancel(self):
        pass

    def acquire(self):
        pass

    def release(self):
        pass


#将普通函数转化成greenlet
def greenlet_patch(fn):
    def call(*args, **kwargs):
        return gevent.spawn(fn, *args, **kwargs);
    return call;

#多线程计时器
class _TimerT(_Timer):
    def __init__(self, delay, fn, *args, **kwargs):
        self._lock = Lock();
        self._delay = delay;
        self._timer = Timer(delay, fn, args=args, kwargs=kwargs);

    def acquire(self):
        self._lock.acquire();

    def release(self):
        self._lock.release();

    def start(self):
        self._timer.start();
        self.exctime = time.time() + self._delay;

    def cancel(self):
        self._timer.cancel();
    

#协程计时器
class _TimerM(_Timer):
    def __init__(self, delay, fn, *args, **kwargs):
        self._timer = gevent.get_hub().loop.timer(delay, 0);
        self._fn = fn;
        self._delay = delay;
        self._args = args;
        self._kwargs = kwargs;

    def start(self):
        self._timer.start(self._call);
        self.exctime = time.time() + self._delay;

    @greenlet_patch
    def _call(self):
        return self._fn(*self._args, **self._kwargs);

    def cancel(self):
        self._timer.stop();

import time
def test(a,b):
    """a test function for timer"""
    print "Test called by %s,%s at %s"%(a,b,time.ctime());
