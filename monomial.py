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
        generators = tuple(generators)
        for i in generators:
            assert re.match(monomial.generatorRE,i)
        self.coefficient = coeff.clean()
        self.generators = generators



    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################
    def clean(self):
        return monomial(self.coefficient.clean(),self.generators)



    def submonomial(self,a,b):
        """Returns the monomial from position a to position b (right hand open).
        e.g. xy._submonomial(0,1) = x. Sets coefficient to one"""
        return self[a:b]

    def withCoefficientOf1(self):
        return self.submonomial(0, len(self.generators))

    def __iter__(self):
        yield self

    def __getitem__(self,index):
        """Access the generators as submonomials"""
        if isinstance(index,slice):
            return monomial(1,self.generators[index])
        return monomial(1,[self.generators[index]])
    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################

    def degree(self):
        return len(self.generators)

    def isAddable(self,other):
        """Tests whether the generator tuples are equal"""
        return self.generators == other.generators


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
            if self.coefficient == -1:
                return '-' + ''.join(self.generators)
            return repr(self.coefficient) + ''.join(self.generators)

    def toLatex(self):
        if self.isZero():
            return "0"
        elif self.degree() == 0:
            return self.coefficient.toLatex()
        else:
            #next two lines add subscripts before numbers
            temp = [re.match(monomial.generatorRE, x) for x in self.generators]
            temp = [ x.group('letter') + '_{' + x.group('digits')+ '}' if x.group('digits') != ''
                    else x.group('letter') for x in temp]
            #next block adds superscripts for repititions
            newTemp = []
            currentCount = 1
            for index, i in enumerate(temp):
                if currentCount > 1:
                    currentCount -= 1
                    continue
                for j in temp[index+1:]:
                    if j == i:
                        currentCount += 1
                    else:
                        break
                if currentCount == 1:
                    newTemp.append(i)
                else:
                    newTemp.append(i + '^{' + str(currentCount) + '}')
            temp = newTemp
            coefficientJoiner = '*'
            if self.coefficient == -1:
                coefficientJoiner = ''
            return self.coefficient.toLatex() + coefficientJoiner + ''.join(temp)


def generators(inString):
    return map(lambda x: monomial(1,x),inString.split(' '))



if __name__ == '__main__':
    pass
