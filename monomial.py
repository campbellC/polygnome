import re
import abstractPolynomial
import coefficient
import polynomial

class monomial(abstractPolynomial.abstractPolynomial):
    """
    File: monomial.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A monomial is basically a coefficient and a tuple of generators.
    """
    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################

    generatorRE = re.compile(r"(?P<letter>[a-zA-Z])(?P<digits>\d*)")

    def __init__(self, coeff=None, generators=() ):
        if not isinstance(coeff,coefficient.coefficient):
            coeff = coefficient.coefficient(coeff)

        if type(generators) is str:
            generators = (generators,)
        assert isinstance(generators, tuple)
        for i in generators:
            assert re.match(monomial.generatorRE,i)
        self.coefficient = coeff.clean()
        self.generators = generators



    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################
    def clean(self):
        return monomial(self.coefficient.clean(),self.generators)



    def submonomial(self,a,b): #returns the monomial from position a to position b (right hand open). e.g. xy._submonomial(0,1) = x. sets coefficient to one

        assert 0 <= a <= len(self.generators)
        assert a <= b <= len(self.generators)
        newGens = self.generators[a:b]
        return monomial(1,newGens)

    def withCoefficientOf1(self):
        return self.submonomial(0, len(self.generators))

    def __iter__(self):
        yield self

    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################

    def degree(self):
        return len(self.generators)

    def isAddable(self,other):
        if self.degree() != other.degree():
            return False
        if self.generators == other.generators:
            return True
        else:
            return False


    def isZero(self):
        return self.coefficient.isZero()

    def __add__(self,other ):
        if isinstance(other,monomial):
            if self.isAddable(other):
                newCoefficient = self.coefficient + other.coefficient
                return monomial(newCoefficient,self.generators)
            else:
                return polynomial.polynomial((self,other))
        elif isinstance(other,coefficient.coefficient) or type(other) in [str,float,int]:
            #in this case we treat whatever we are adding as though it is a
            #coefficient lying in the underlying field
            return self + monomial(other)
        else:
            return NotImplemented



    def __mul__(self,other):
        if isinstance(other,monomial):
            newCoeff = self.coefficient * other.coefficient
            newGenerators = self.generators + other.generators
            return monomial(newCoeff,newGenerators)

        elif isinstance(other,coefficient.coefficient) or type(other) in [float,int,str]:
           return self * monomial(other)

        else:
            return NotImplemented

    def __rmul__(self,other):
            return self * other #this case should only hit for coefficients or numbers in which case the multiplication is commutative
    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################


    def __repr__(self): # TODO: add the +1 -1 stuff here.
        if self.isZero():
            return "0"
        elif self.degree() == 0:
            return repr(self.coefficient)
        else:
            if self.coefficient == 1:
                return ''.join(self.generators)
            coefficientJoiner = '*'
            if self.coefficient == -1:
                coefficientJoiner = ''
            return repr(self.coefficient) + coefficientJoiner + ''.join(self.generators)

    def toLatex(self):
        if self.isZero():
            return "0"
        elif self.degree() == 0:
            return self.coefficient.toLatex()
        else:
            temp = map(lambda x: re.match(monomial.generatorRE, x), self.generators)
            temp = map( lambda x: x.group('letter') + '_{' + x.group('digits')+ '}', temp)
            coefficientJoiner = '*'
            if self.coefficient == -1:
                coefficientJoiner = ''
            return self.coefficient.toLatex() + coefficientJoiner + ''.join(temp)


def generators(inString):
    return map(lambda x: monomial(1,x),inString.split(' '))



if __name__ == '__main__':
   x1 = monomial('q','x1')
   print x1
   x2 = monomial(1,'x2')
   y = x2 * x1
   print y.toLatex()
