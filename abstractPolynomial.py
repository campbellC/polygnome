from abc import ABCMeta, abstractmethod
import arithmeticInterface

class abstractPolynomial(arithmeticInterface.arithmeticInterface):
    __metaclass__ = ABCMeta
    """
    File: abstractPolynomial.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: An abstract superclass for polynomials and monomials.
    Most of the methods must be instantiated for yourself.
    """
    @abstractmethod
    def __iter__(self): pass
