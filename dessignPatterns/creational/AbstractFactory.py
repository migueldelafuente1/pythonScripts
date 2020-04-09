'''
Created on 7 abr. 2020

@author: Miguel
'''

''' When there are same objects with different behavior on the context, simple
    Factory classes usually get a cumbersome situation; usually with lots of 
    factories to be tracked and having to set explicitly the values for the 
    context.
    
    In this situation, the abstract factory encapsulates both the creation and 
    the relations with the global context.
    
    Definition: Dessing Pattern that provide an interface to create object 
    families with interdependence (between themselves) without specifying their 
    concrete class.
    
    With this creational pattern, we work with the abstraction of the objects. 
    '''
    
## EXAMPLE OF USE OF THEMES OF APP (Dark theme, white theme)
#------------------------------------------------------------------------------ 

#===============================================================================
#     OBJECTS
#===============================================================================

class Cursor:
    color   = None
    pointer = None
    
    def __init__(self):
        raise Exception("Cannot create abstract cursor")
    
    def click(self):
        self._click = True

OBJECTS_BAR = {'users': ['Alice', 'Bob', 'Charley'], 
               'info': 'User login app', 
               'software language': 'python 3'}

class NavBar:
    
    color  = None
    symbol = None
    
    def __init__(self):
        raise Exception("Cannot create abstract nav bar")
    
    def getResult(self, search_str):
        if search_str:
            result = OBJECTS_BAR.get(search_str.lower())
            if not result:
                return "'{}' not found".format(search_str)
            return result
        else:
            return "Item for search not given. Try again"

class DarkCursor(Cursor):
    
    color   = 'grey'
    pointer = 'Standard'
    
    def __init__(self):
        print("Dark Cursor selected")
        self._click = False

class WhiteCursor(Cursor):
    
    color   = 'white'
    pointer = 'Mode_St3'
    
    def __init__(self):
        print("White Cursor selected")
        self._click = False

class DarkNavBar(NavBar):
    
    color  = 'white_grey'
    text   = 'white'
    symbol = 'lens'
    
    def __init__(self):
        print("Instance Dark Navigation Bar")
        
class WhiteNavBar(NavBar):
    
    color  = 'white'
    text   = 'black'
    symbol = 'eye'
    
    def __init__(self):
        print("Instance White Navigation Bar")
    
#===============================================================================
#     ABSTRACT FACTORIES
#===============================================================================

class ThemeAbstractFactory():
    '''
    defines all the creators without specifying the object creator:
    '''
    @classmethod
    def createNavBar(cls):
        """
        :return NavBar Instance"""
        raise Exception("abstract creator for Nav Bars")


    @classmethod
    def createCursor(cls):
        """
        :return NavBar Instance"""
        raise Exception("abstract creator for Nav Bars")
    
    
class DarkThemeFactory(ThemeAbstractFactory):
    
    @classmethod
    def createNavBar(cls):
        return DarkNavBar()
    
    @classmethod
    def createCursor(cls):
        return DarkCursor()

class WhiteThemeFactory(ThemeAbstractFactory):
    
    @classmethod
    def createNavBar(cls):
        return WhiteNavBar()
    
    @classmethod
    def createCursor(cls):
        return WhiteCursor()



def actions_client(themeFactory):
    
    cursor = themeFactory.createCursor()
    navBar = themeFactory.createNavBar()


print(">> client selects the code in dark theme")
actions_client(DarkThemeFactory)

print(">> client selects the code in white theme")
actions_client(WhiteThemeFactory)
