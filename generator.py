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

    def __init__(self,string,number=None,algebra=None):
        assert isinstance(string,str)
        assert isinstance(number,int) or number is None
        self.string = string
        self.number = number
        self.algebra = algebra

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
    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################

    def __repr__(self):
        ret = self.string
        if self.number is not None:
            ret = ret + str(self.number)
        return ret

    def toLatex(self):
        ret = self.string
        if self.number is not None:
            ret = ret + "_{" + str(self.number) + "}"
        return ret


if __name__ == '__main__':
    x = generator("x",1)
    y = generator("y",1000)
    #z = generator("", 2000)

    print x.toLatex()
    print x

