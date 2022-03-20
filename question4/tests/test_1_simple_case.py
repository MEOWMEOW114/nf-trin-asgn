"""test suite for rtanalysis
"""

import pytest
from lrucache.lrucache import LruCache

def test_simple():
    cache = LruCache(2)
    print(cache.cache)
    cache.put(1, 11)
    cache.get(1)
    print(cache.cache)
    cache.put(3, 3)
    cache.put(4, 3)
    cache.put(4, 4)
    print(cache.cache)
    assert cache.get(1) is None
    assert cache.get(4) == 4