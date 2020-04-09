'''
Created on 7 abr. 2020

@author: Miguel
'''
from __future__ import annotations
from abc import ABC, abstractmethod


class OperationStrategy(ABC):
    '''
    Strategy interface, declares abstract operations
    '''
    @staticmethod
    @abstractmethod
    def add(*args):
        pass
    
    @staticmethod
    @abstractmethod
    def multiply(constant, A):
        pass

class ArrayOperation(OperationStrategy):
    
    @staticmethod
    def add(A, B):
        if len(A) != len(B):
            raise Exception("len(A)[{}] != len(B)[{}]".format(len(A), len(B)))
        aux = [0]*len(A)
        for i in range(len(A)):
            aux[i] = A[i]+B[i]
        return aux
    
    @staticmethod
    def multiply(constant, array):
        aux = [0]*len(array)
        for i in range(len(array)):
            aux[i] = array[i]*constant
        return aux
        
class IntegerOperation(OperationStrategy):
    
    @staticmethod
    def add(A, B):
        return A + B
    
    @staticmethod
    def multiply(constant, A):
        return constant*A
    

class Context():
    
    """ Context defines the global logic between elements, based on the
    external choice of strategy (within here, it is not specified)"""
    def __init__(self, strategy: OperationStrategy):
        
        self._strategy = strategy
        
        
    @property
    def strategy(self):
        return self._strategy
    
    
    def computeOperationValues(self, A, B):
        
        result = self._strategy.add(A, B)
        result = self._strategy.multiply(2.5, result)
        
        print("result:", result)
        
if __name__ == "__main__":
    cInt = Context(IntegerOperation)
    cInt.computeOperationValues(1, 3)
    
    cList = Context(ArrayOperation)
    cList.computeOperationValues([1, 2, 3], [10, 9, 8])
    