import polygnomeObject
import abstractPolynomial

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

    def __init__(self,LHS,RHS):
        assert isinstance(RHS,abstractPolynomial.abstractPolynomial)
        assert isinstance(LHS,abstractPolynomial.abstractPolynomial)
        assert RHS.algebra is None
        assert LHS.algebra is None
        self.LHS = LHS
        self.RHS = RHS

    def __repr__(self):
        return repr(self.LHS-self.RHS)

    def toLatex(self):
        return (self.LHS-self.RHS).toLatex()

    ##############################################################################
    ######  ACTION CODE
    ##############################################################################

    def doesAct(self,poly): #some iterable containing symbols
    	poly = poly.changeAlgebra(None)
        return (poly - self.LHS).isZero()

    def act(self,poly):
        if self.doesAct(poly):
            return self.RHS
        else:
            return poly

if __name__ == '__main__':
    pass
