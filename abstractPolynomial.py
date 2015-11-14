from abc import ABCMeta, abstractmethod
import polygnomeObject

class abstractPolynomial(polygnomeObject.polygnomeObject):
    __metaclass__ = ABCMeta
    """
    File: abstractPolynomial.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: An abstract superclass for polynomials, monomials, generators and coefficients.
    Most of the methods must be instantiated for yourself.
    """


    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################
    def isSorted(self):
        return True

    def sort(self):
        return self

    @abstractmethod
    def changeAlgebra(self,algebra): pass

    def free(self):
        return self.changeAlgebra(None)


    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################
    @abstractmethod
    def isZero(self): pass

    def __eq__(self,other):
        x = self - other
        x = x.sort()
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
    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################

    @abstractmethod
    def __repr__(self): pass

    @abstractmethod
    def toLatex(self): pass
