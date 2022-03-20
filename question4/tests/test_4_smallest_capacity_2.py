"""test suite for rtanalysis
"""

import pytest
from lrucache.lrucache import LruCache

def test_simple():
    cache = LruCache(0)
    print(cache.cache)
    cache.put(1, 2)
    assert cache.get(1) is not None
