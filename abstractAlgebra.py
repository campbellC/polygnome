from abc import ABCMeta, abstractmethod
import polygnomeObject
import relation
import reductionFunction

class abstractAlgebra(polygnomeObject.polygnomeObject):
    __metaclass__ = ABCMeta
    """
    File: abstractAlgebra.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: An abstract superclass for algebras and tensor products of algebras etc.
    """
    @abstractmethod
    def __iter__(self): pass

    def equivalent(self,polynomial1,polynomial2):
        return self.reduce(polynomial1) == self.reduce(polynomial2)

    @abstractmethod
    def makeReductionFunction(self,polynomial1): pass

    @abstractmethod
    def makeReductionSequence(self,polynomial1): pass

    @abstractmethod
    def reduce(self,polynomial1): pass




if __name__ == '__main__':
    pass
