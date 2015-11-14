import re
import monomial
import abstractPolynomial

class generator(abstractPolynomial.abstractPolynomial):
    """
    File: generator.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A generator for an algebra over some coefficient ring. These generators are always a
    nonempty string with possibly a number associated (e.g. alpha_1, x, y, q_10000).

    If ever used as an actual symbol to be manipulated it defaults to being the monomial with it's value and a coefficient of 1.
    """
    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################
    def __init__(self, string, algebra=None):
        nameRE = re.compile(r"(?P<letters>[a-zA-Z])*(?P<digits>\d*)")

        match = re.match(nameRE,string)
        assert match

        self.letters = match.group('letters')
        self.digits = match.group('digits')
        self.name = string
        self.algebra = algebra

    def changeAlgebra(self,alg):
        return generator(self.name,alg)

    def clean(self):
        return monomial.monomial.fromGenerator(self)

    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################

    def isZero(self):
        return False

    def __add__(self,other):
        new = monomial.monomial.fromGenerator(self)
        return new + other


    def __mul__(self,other):
        new = monomial.monomial.fromGenerator(self)
        return new * other

    def __rmul__(self,other):
        new = monomial.monomial.fromGenerator(self)
        return other * new

    def __iter__(self):
        return monomial.monomial.fromGenerator(self)
    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################

    def __repr__(self):
        return self.name

    def toLatex(self):
        return self.letters + '_{' + self.digits + '}'


if __name__ == '__main__':
    x = generator("x1")
    y = generator("y1000")
    #z = generator("", 2000)

    print x.toLatex()
    print x

