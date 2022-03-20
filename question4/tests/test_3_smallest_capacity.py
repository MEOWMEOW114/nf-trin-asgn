"""test suite for rtanalysis
"""

import pytest
from lrucache.lrucache import LruCache

def test_simple():
    cache = LruCache(1)
    print(cache.cache)
    cache.put(1, 2)
    print(cache.cache)
    cache.put(3, 3)
    assert cache.get(1) is None
