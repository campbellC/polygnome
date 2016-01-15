import abstractPolynomial
import monomial
import coefficient
import composite
class polynomial(composite.composite,abstractPolynomial.abstractPolynomial):
    """
    File: polynomial.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: The polynomial class composite class for abstractPolynomials.
    """
    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################

    def __init__(self,monomials=()):
        if isinstance(monomials, monomial.monomial):
            monomials = (monomials,)
        monomials = tuple(monomials)
        composite.composite.__init__(self,monomials)
        self.monomials = self.components




    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################


    def __mul__(self, other):
        if len(self) == 0:
            return self
        if isinstance(other,monomial.monomial) or (type(other) in [str,float,int]) or isinstance(other,coefficient.coefficient):
            newMonos = []
            for i in self:
                newMonos.append(i * other)
            return polynomial(tuple(newMonos)).clean()
        if isinstance(other,polynomial):
            if len(other.monomials) == 0:
                return other
            newMonos = []
            for mono1 in self:
                for mono2 in other.monomials:
                    newMonos.append(mono1 * mono2)
            return polynomial(tuple(newMonos)).clean()
        # From here on we know length of monomials > 0


    def __rmul__(self,other):
        if isinstance(other,monomial.monomial):
            other = polynomial(other)
            return (other * self).clean()
        elif (type(other) in [str,float,int]) or isinstance(other,coefficient.coefficient):
            return self * other
        else:
            return NotImplemented

    def __add__(self,other):
        if isinstance(other,abstractPolynomial.abstractPolynomial):
            return composite.composite.__add__(self,other)

        elif (type(other) in [str,float,int]) or isinstance(other,coefficient.coefficient):
            return self + monomial.monomial(other)

        else:
            return NotImplemented



if __name__ == '__main__':
    pass
