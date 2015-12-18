import abstractPolynomial
import monomial
import coefficient

class polynomial(abstractPolynomial.abstractPolynomial):
    """
    File: polynomial.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: The polynomial class is mainly a container for monomials.
    """
    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################

    def __init__(self,monomials=()):
        if isinstance(monomials, monomial.monomial):
            monomials = (monomials,)

        assert isinstance(monomials,tuple)
        self.monomials = monomials



    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################
    def __iter__(self):
        for i in self.monomials:
            yield i


    def clean(self):
        newMonos = []
        for index, mono in enumerate(self): #iterate through monomials
            for j in newMonos: #check if we've seen this before
                if mono.isAddable(j):
                    break
            else: # if we haven't seen this before, take all of the monomials with
                # the same generators and add them all together
                for index2, mono2 in enumerate(self):
                    if index >= index2:
                        continue
                    else:
                        if mono.isAddable(mono2):
                            mono = mono + mono2
                newMonos.append(mono.clean())
        newMonos = filter(lambda x: not x.isZero(), newMonos)
        return polynomial(tuple(newMonos))

    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################

    def isZero(self):
        other = self.clean()
        return len(other.monomials) == 0

    def __mul__(self,other):
        if len(self.monomials) == 0:
            return self
        if isinstance(other,monomial.monomial) or (type(other) in [str,float,int]) or isinstance(other,coefficient.coefficient):
            newMonos = []
            for i in self.monomials:
                newMonos.append(i * other)
            return polynomial(tuple(newMonos)).clean()
        if isinstance(other,polynomial):
            if len(other.monomials) == 0:
                return other
            newMonos = []
            for mono1 in self.monomials:
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
        if isinstance(other,polynomial):
            newMonos = self.monomials + other.monomials
            return polynomial(newMonos).clean()

        if isinstance(other,monomial.monomial):
            return self + polynomial(other)
        elif (type(other) in [str,float,int]) or isinstance(other,coefficient.coefficient):
            return self + monomial.monomial(other)
        else:
            return NotImplemented

    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################

    def __repr__(self):
        if self.isZero():
            return '0'
        return "+".join(x.__repr__() for x in self if not x.isZero())

    def toLatex(self):
        if self.isZero():
            return "0"
        return "+".join(x.toLatex() for x in self if not x.isZero())

if __name__ == '__main__':
    x1 = monomial.monomial(1,'x1')
    x2 = monomial.monomial(1,'x2')
    y = x1*x2
    z = x2*x1 *'q'
    xy = y + z * z + y
    print "xy=" , xy.toLatex()
    print xy.clean()
    print "xy ^ 2= " , (xy * xy).toLatex()
    print xy-(xy + 'q') * 2
