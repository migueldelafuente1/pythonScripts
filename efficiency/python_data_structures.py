from time import time

def timer(function, *args):
    N = 1000
    tic_ = time()
    for _ in range(N):
        function(*args)
    print("\tfunction [",function.__name__,"]:\t",(time()-tic_)*(N/1000),' us')
# =============================================================================
#   Lists and Queues
# =============================================================================
N_max = 10000


print("\nLISTS:")
lists = {
        'list_1': [i for i in range(N_max)],
        'list_3': [i for i in range(3 * N_max)]
        }

for name, a in lists.items():
    print(">>", name, " [",len(a),"]")
    timer(a.pop)                # O(1)
    timer(a.pop, 1)             # O(N)
    timer(a.append, 1)          # O(1) - if there is no realocation, else O(N)
    timer(a.insert, 0, 1)       # O(N)

print("\nQUEUES:")
from collections import deque
queues = {
        'queue_1': deque([i for i in range(N_max)]),
        'queue_3': deque([i for i in range(3 * N_max)])
        }

for name, a in queues.items():
    print(">>", name, " [",len(a),"]")
    timer(a.pop)                # O(1)
    timer(a.popleft)            # O(1)
    timer(a.append, 1)          # O(1) - if there is no realocation, else O(N)
    timer(a.appendleft, 1)      # O(1)
    
""" deque has a cost on getting items by index: [i] in the middle of the 
the array 
"""

for name, a in queues.items():
    print(">>", name, " [",len(a),"],   __getitem__()")
    timer(a.__getitem__, 0)                 # O(1)
    timer(a.__getitem__, len(a)-1)          # O(1)
    timer(a.__getitem__, int(0.5*len(a)))   # O(N)


# =============================================================================
#   Bisect Module
# =============================================================================

import bisect
print("\nbisect method return the index for the new value in an ordered list.\n"
      "It is based on the binnary algorithm")
collection = [1, 2, 4, 5, 6]
print(collection)
print(bisect.bisect(collection, 3))     # O(log(N))
print(collection)

lists = {
        'list_1': [i for i in range(N_max)],
        'list_3': [i for i in range(3 * N_max)]
        }
for name, a in lists.items():
    print(">>", name, " [",len(a),"],   __getitem__() vs bisect")
    timer(a.index, N_max-1)                # O(N)
    timer(bisect.bisect, a, len(a)-1)      # O(log(N))

# =============================================================================
#   Dictionaries
# =============================================================================

for i in range(10):
    print(hash("kk"+str(i)), "\tnorm up to 10: ", hash("kk"+str(i)) % 10)
    
"""
The defaultdict will create any items that you try to access (provided of course 
they do not exist yet). It won't throw KeyError exeception.
"""

from collections import defaultdict
d_dict = defaultdict(float) # or  list, float, dict, set, ...
for s in "adjjddaadl":
    #d_dict[s].add(s)
    #d_dict[s].append(s)
    #d_dict[s][s] = s
    d_dict[s] += 1                  # O(N)
    
print(d_dict)
from collections import Counter
d_dict = Counter('asdasdsd')        # O(N)
print(d_dict)

## Building an in-memory search index using a hash map

docs = ["the cat is under the table",
        "the dog is under the table",
        "cats and dogs smell roses",
        "Carla eats an apple"]
# Building an index
index = {}
for i, doc in enumerate(docs):
    # We iterate over each term in the document
    for word in doc.split():
        # We build a list containing the indices
        # where the term appears
        if word not in index:
            index[word] = [i]
        else:
            index[word].append(i)

print(index)
results = index["table"]        # O(1) search (system limited by memory size)
result_documents = [docs[i] for i in results]

# =============================================================================
#   Sets
# =============================================================================
print("\nSets")
s = [1, 2, 3, 5, 1, 3]
t = [3, 5, 5, 3]

s = set(s)
t = set(t)

print(s.union(t))           # O(S+T)
print(s.intersection(t))    # O(min(T, S))
print(s.difference(t))      # O(S)

# Building an index using sets
index = {}
for i, doc in enumerate(docs):
    # We iterate over each term in the document
    for word in doc.split():
        # We build a set containing the indices
        # where the term appears
        if word not in index:
            index[word] = {i}
        else:
            index[word].add(i)

# Querying the documents containing both "cat" and "table"
index['cat'].intersection(index['table'])
print(index)

# =============================================================================
#  Heaps
# =============================================================================
#   A heap is a more efficient data structure that allows for insertion and 
# extraction of maximum values with O(log(N)) time complexity.

import heapq
collection = [10, 3, 3, 4, 5, 6]
heapq.heapify(collection)

print(heapq.heappop(collection))
heapq.heappush(collection, 1)

# Other easy option is the queue.PriorityQueue that is thread and process-safe.

from queue import PriorityQueue
queue = PriorityQueue()
for element in collection:
    queue.put(element)
print(queue.get())
print(queue.get())
print(queue.get())

queue = PriorityQueue()
queue.put((3, "priority 3"))
queue.put((2, "priority 2"))
queue.put((1, "priority 1"))

print(queue.get())

# =============================================================================
#   Tries 
# =============================================================================
#   Tree data structure that keeps strings (len=i) which their childs are 
# extensions (len=i+1) of the parent node. These relations are useful to search 
# possibilities for a certain  characters (in a certain order)
# 
#
#from patricia import trie
#strings_dict = {s:0 for s in strings}
## A dictionary where all values are 0
#strings_trie = trie(**strings_dict)

class TrieNode:
    
    def __init__(self, string, booking_index, level):
        
        self.__children   = {}
        self.__level    = level
        self.__node     = string[0] if level > 0 else ''
#         if len(string) < level:
#             raise Exception("string is shorter than the curren node level: "
#                             "[{}] local length={}".format(string, level))
        if len(string) == 0:
            self.__addBookingIndex(booking_index)
        else:
            ## append TrieNode child
            string = string[1:] if level > 0 else string
            self.__appendChild(string, booking_index, level)
    
    def add(self, string, booking_index):
        self.__appendChild(string, booking_index, 0)
    
    ## Searh algotirhm 
    def search(self, string):
        
        if len(string) == 0:
            return self.__indexes
        else:
            if string[0] in self.__children:
                return self.__children[string[0]].search(string[1:])
            else:
                return None
    
    ## Child append
    def __appendChild(self, string, booking_index, level):
        if len(string) == 0:
            self.__addBookingIndex(booking_index)
        else:    
            if string[0] in self.__children:
                self.__children[string[0]].__appendChild(string[1:], 
                                                                booking_index, 
                                                                level+1)
            else:
                self.__children[string[0]] = TrieNode(string, 
                                                      booking_index, 
                                                      level+1)
    ## Location append         
    def __addBookingIndex(self, booking_index):
        if hasattr(self, '_TrieNode__indexes'):
            self.__indexes.add(booking_index)
        else:
            self.__indexes = set([booking_index])
    
    def printTree(self):
        _tab = ''.join(['·']*self.__level)
        _indx_str = ''
        if hasattr(self,'_TrieNode__indexes'):
            _indx_str = self.__indexes
        
        print(_tab, "<{}> {}".format(self.__node, _indx_str))
        for child in self.__children.values():
            child.printTree()
    
class Trie:
    
    def __init__(self, string, booking_index):
        self.__root = TrieNode(string, booking_index, level=0)
    
    def search(self, string):
        """ Return booking index of the exact string or None if it's not in """
        return self.__root.search(string)
    
    def add(self, string, booking_index):
        self.__root.add(string, booking_index)
        
    def printTrie(self):
        self.__root.printTree()
    

print("\nTries::")
trie = Trie('aasd', 10)
trie.add('aasd', 20)
trie.add('a2sd', 21)

_str = 'aasd'
print("index for:", _str, " -> ", trie.search(_str))
trie.add('as', 99)
trie.add('as sd', 88)
trie.printTrie()