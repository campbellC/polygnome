import polygnomeObject
import monomial
import abstractPolynomial

class relation(polygnomeObject.polygnomeObject):
    """
    File: relation.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A quadratic relation in the free algebra that will be used to reduce monomials.
    """
    def __init__(self,mono,poly):
        self.LHS = mono
        self.RHS = poly
        self.sanityCheck()

    def __repr__(self):
        return (self.LHS - self.RHS).__repr__()

    def toLatex(self):
        return (self.LHS - self.RHS).toLatex()

    def sanityCheck(self):
        assert issubclass(self.mono,monomial.monomial)
        assert self.mono.coefficient == 1
        assert issubclass(self.poly,abstractPolynomial.abstractPolynomial)

