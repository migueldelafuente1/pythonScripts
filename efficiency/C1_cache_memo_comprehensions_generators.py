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
print("CACHE: time 400!*", N, "=",  min(results),'us(min),',
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

N = 5# 20# 
print("COMPREHENSIONS:")

"""
Generators and Comprehension are preferred in place of explicit for-loops 
More readable, more efficient compared with the explicit loop.
Efficient looping (in memory) by ITERATORS and  map, filter... functions

:List_Comprehension have to allocate in memory the new list
:Generators are objects that compute the value on the fly and returns the result
    when called. map, filter, reduce... uses a function and an ITERABLE.
    The opperation happens when we are iterating, not when map is invoqued
    
itertools functions in python 3 are all generators
"""

def loop():
    res = []
    for i in range(N):
        res.append(i * i)
    return sum(res)
def loop_dict():
    res = {}
    for i in range(N):
        res[i] = i**2
    return res

print("loop (list)", N, ":\t\t", timeit.timeit(loop))
print("loop (dict)", N, ":\t\t", timeit.timeit(loop_dict))
"""Comprehension form iterables over applications"""
def comprehension():
    return sum([i * i for i in range(N)])
def comprehension_dict():
    return sum({i: i**2 for i in range(N)})
print("comprehension (list)", N, ":\t", timeit.timeit(comprehension))
print("comprehension (dict)", N, ":\t", timeit.timeit(comprehension_dict))
#===============================================================================
#     GENERATORS
#===============================================================================
"""The generator lead an iterator for yielding an operation."""
def generator():
    return sum(i * i for i in range(N))
print("generator (list)", N, ":\t\t", timeit.timeit(generator))



#===============================================================================
#     Comparative map+Generators vs Comprehension lists
#===============================================================================

## MEMORY PROFILER: ____________________________________________________________
from memory_profiler import profile

@profile(precision=5)
def map_normal(numbers):
    a = map(lambda n: n * 2, numbers)
    b = map(lambda n: n ** 2, a)
    c = map(lambda n: n ** 0.33, b)
    return max(c)

@profile(precision=5)
def map_comprehension(numbers):
    a = [n * 2 for n in numbers]
    b = [n ** 2 for n in a]
    c = [n ** 0.33 for n in b]
    return max(c)

numbers = range(1000000)
map_normal(numbers)
map_comprehension(numbers)

# TO VIEW THE MEMORY IMPACT 
# run: python -m memory_profiler cache_memo_comprehensions_generators.py
# 
# OUTPUT# 
# Line #    Mem usage    Increment   Line Contents
# ================================================
#    142  43.10547 MiB  43.10547 MiB   @profile(precision=5)
#    143                             def map_normal(numbers):
#    144  43.17969 MiB   0.00781 MiB       a = map(lambda n: n * 2, numbers)
#    145  43.17578 MiB   0.00781 MiB       b = map(lambda n: n ** 2, a)
#    146  43.19531 MiB   0.02344 MiB       c = map(lambda n: n ** 0.33, b)
#    147  43.16406 MiB   0.00000 MiB       return max(c)
# 
# Line #    Mem usage    Increment   Line Contents
# ================================================
#    149  43.16406 MiB  43.16406 MiB   @profile(precision=5)
#    150                             def map_comprehension(numbers):
#    151  81.76953 MiB   0.44141 MiB       a = [n * 2 for n in numbers]
#    152 121.09766 MiB   0.48828 MiB       b = [n ** 2 for n in a]
#    153 152.24609 MiB   0.62500 MiB       c = [n ** 0.33 for n in b]
#    154 152.24609 MiB   0.00000 MiB       return max(c)



