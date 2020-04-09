'''
Created on 7 abr. 2020

@author: Miguel
'''



'''
    Factory classes are use to encapsulate the strategies for the creation of 
    objects, the "fabrication" strategy can be over written by each Concrete 
    Factory class that implements the abstract factory for the object.
    '''

#===============================================================================
#     PRODUCTS
#===============================================================================
class Pizza:
    
    def __init__(self):
        raise Exception('Abstract method, cannot create abstract pizza')
    
    @property
    def ingredients(self):
        return self._ingredients
    @property
    def mass(self):
        return self._mass
    @property
    def oven_cooked(self):
        return self._cooked
    
    def eat(self):
        raise Exception('Abstract method, cannot eat abstract pizza')
    def bake(self):
        raise Exception('Abstract method, cannot bake abstract pizza')

class HawaianPizza(Pizza):
    def __init__(self):
        self._ingredients = ['pineapple', 'cheese', 'tomato']
        self._mass = 'thin'
        self._cooked = True
    
    def bake(self):
        if not self._cooked:
            self._cooked = True
    
    def eat(self):
        print(' hawaian pizza has been eaten')
        self = None

class FourCheesePizza(Pizza):
    def __init__(self):
        self._ingredients = ['cheese1', 'cheese2', 'mozarella', 'cheese4', 'tomato']
        self._mass = 'thick'
        self._cooked = True
    
    def bake(self):
        if not self._cooked:
            self._cooked = True
    
    def eat(self):
        print('pizza 4 cheese has been eaten')
        self = None

#===============================================================================
#    FACTORIES
#===============================================================================
class PizzaFactory:
    
    @classmethod
    def createPizza(cls):
        raise Exception('Abstract factory cannot deliver abstract pizza')
    
    
class RandomPizzaFactory(PizzaFactory):
    
    @classmethod
    def createPizza(cls):
        from numpy import random
        if random() < 0.5:
            return HawaianPizza()
        else:
            return FourCheesePizza()

class HawaianPizzaFactory(PizzaFactory):
    
    @classmethod
    def createPizza(cls):
        return HawaianPizza()

class CostumerPizzaFactory(PizzaFactory):
    @classmethod
    def createPizza(cls, pizza):
        if pizza == 'hawaian':
            return HawaianPizza()
        elif pizza == '4cheese':
            return FourCheesePizza()
        else:
            return None
        