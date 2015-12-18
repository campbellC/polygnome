from abc import ABCMeta, abstractmethod
import polygnomeObject
class arithmeticInterface(polygnomeObject.polygnomeObject):
    __metaclass__ = ABCMeta
    """
    File: arithmeticInterface.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A simple arithmetic interface that polynomials, tensors,
    vectors, and coefficients will have to implement.
    """


    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################

    def clean(self):   #This is the method that checks if for example we have x + x and simplifies it to 2 x.
        return self

    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################
    @abstractmethod
    def isZero(self): pass

    def __eq__(self,other):
        x = self - other
        x.clean()
        if x.isZero():
            return True
        else:
            return False


    @abstractmethod
    def __add__(self,other): pass

    @abstractmethod
    def __mul__(self,other): pass

    def __sub__(self,other):
        return self + (other * (-1))

    def __radd__(self,other): #addition is always commutative
        return self + other
