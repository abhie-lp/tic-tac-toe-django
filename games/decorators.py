from time import perf_counter


def timeit(method):
    def timed(*args, **kw):
        ts = perf_counter()
        result = method(*args, **kw)
        te = perf_counter()
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te - ts))
        return result

    return timed
