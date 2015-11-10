import polygnomeObject
import monomial
import abstractPolynomial
import generator

class relation(polygnomeObject.polygnomeObject):
    """
    File: relation.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A quadratic relation in the free algebra that will be used to reduce monomials.
    """
    ##############################################################################
    ######  polygnomeObject code
    ##############################################################################
    def __init__(self,gen1,gen2,poly):
        assert isinstance(gen2, generator.generator)
        assert isinstance(gen1, generator.generator)
        assert issubclass(poly, abstractPolynomial.abstractPolynomial)
        self.generator1 =gen1
        self.generator2 = gen2
        self.LHS = monomial.fromGenerator(gen1) * monomial.fromGenerator(gen2)
        self.RHS = poly


    def __repr__(self):
        return (self.LHS - self.RHS).__repr__()

    def toLatex(self):
        return (self.LHS - self.RHS).toLatex()

    ##############################################################################
    ######  ACTION CODE
    ##############################################################################

    def doesAct(self,gen1,gen2): #Check if this relation can act on a pair of generators
        return gen1 == self.generator1 and gen2 == self.generator2

    def act(self,gen1,gen2):
        return self.RHS

