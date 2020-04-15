'''
Created on 15 abr. 2020

@author: Miguel
'''
import numpy as np
import timeit
import time
import itertools
#===============================================================================
#     CACHING
#===============================================================================
"""
Cache save in memory/disk ongoing states of a program, to save resource costs 
of loading, computing ...

use of functools.lru_cache (decorator) for results of a function

lru = Last Recently Used

CacheInfo(hits=0, misses=6, maxsize=3, currsize=3)
"""

from functools import lru_cache

def factorial_raw(n, log=True):
    if log: 
        print("Actual compute n=", n)
    if n > 1:
        return np.log(n) + factorial_raw(n-1,log)
    return 0

@lru_cache(maxsize=None)
def factorial(n, log=True):
    if log: 
        print("Actual compute n=", n)
    if n > 1:
        return np.log(n) + factorial(n-1,log)
    return 0

""" change max size to 3, 2, ..."""
for _iter in range(6):
    print(f"iter {_iter}: {6-_iter}!=")
    print(factorial.cache_info())
    print(factorial(6-_iter))
    
tic_ = time.time()
_aux = None
N = 100
for f in itertools.repeat(factorial_raw, N):
    f(400, False)
print("RAW:   time 400!*", N, "=", (time.time() - tic_),'s')
tic_ = time.time()
for f in itertools.repeat(factorial, 100*N):
    f(400, False)


print("CACHE: time 400!*", 100*N, "=",  (time.time() - tic_),'s')

setup_code = '''
from functools import lru_cache
from __main__ import factorial_raw
factorial_memoized = lru_cache(maxsize=None)(factorial_raw)
'''
results = timeit.repeat('factorial_memoized(400, False)', setup=setup_code,
                        repeat=100*N, number=1)
print("CACHE: time 400!*", 100*N, "=",  min(results),'us(min),',
      max(results),'us(max)')

## ON DISK CACHE: Jobib
"""
Install:
pip install joblib

Use: The same as lru, but indicating the path to store the cache.
    Limits recomputation only when arguments change. Usefull for np.arrays
    Disk will always be slower than Dynamic Memory Allocation.

from joblib import Memory
memory = Memory(cachedir='/path/to/cachedir')
@memory.cache
def sum2(a, b):
    return a + b
"""

#===============================================================================
#     MEMORIZATION
#===============================================================================

#===============================================================================
#     COMPREHENSIONS
#===============================================================================

#===============================================================================
#     GENERATORS
#===============================================================================
