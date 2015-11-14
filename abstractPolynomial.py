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
        if self.algebra is None:
            return True
        else:
            return self.algebra.doesAct(self)

    def reductionSequence(self):
        if self.isSorted():
            return []
        else:
            f = self.algebra.makeReductionFunction(self)
            return [f] + f(self).reductionSequence()

    def sort(self): # This will completely reduce self using all PBW relations
        x = self.clean()
        for i in self.reductionSequence():
            x = i(x)
        return x

    @abstractmethod
    def clean(): pass  #This is the method that checks if for example we have x + x and simplifies it to 2 x. This does not apply pbw relations.

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
