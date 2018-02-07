import os
import pickle
import xxhash
from functools import wraps


class CacheFunc(object):
    def __init__(self, func, cachedir):
        self.func = func
        self.cachedir = cachedir
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        files = args[0].files
        call_hash = self.calc_hash(files, args, kwargs)
        response = False
        for path, dirs, files in os.walk(self.cachedir):
            for f in files:
                if call_hash == f:
                    print("cached object found: ", call_hash)
                    with open(os.path.join(path, f), "rb") as of:
                        response = pickle.load(of)
        if response == False:
            response = self.func(*args, **kwargs)
            fn = os.path.join(self.cachedir, call_hash)
            with open(fn, "wb") as f:
                pickle.dump(response, f)

        return response

    def calc_hash(self, files, args, kwargs):
        try:
            string = "".join([s.calc_checksum() for s in files] +
                             [str(a) for a in args[1:]] +
                             [str(k) + str(v) for k, v in kwargs.items()])
            cmd_hash = xxhash.xxh64(string, seed=1).hexdigest()
            return cmd_hash

        except TypeError:
            raise TypeError
