import monomial
import abstractPolynomial

class generator(abstractPolynomial.abstractPolynomial):
    """
    File: generator.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A generator for an algebra over some coefficient ring. These generators are always a
    nonempty string with possibly a number associated (e.g. alpha_1, x, y, q_10000)
    """
    ##############################################################################
    ######  Polygnome object methods
    ##############################################################################

    def __init__(self,string,number=None):
        self.string = string
        self.number = number
        self.sanityCheck()

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
    #TODO:add a to monomial function, or make a monomial constructor fromGenerator

    def sanityCheck(self):
        assert isinstance(self.string,str) #generators must have a string
        assert self.string != "" #generators cannot have the empty string as their string
        assert type(self.number) is int or self.number is None #a generator must have an integer or no number associated

    ##############################################################################
    ######  abstractPolynomial methods
    ##############################################################################
    def isZero(self):
        return False


    def __add__(self,other):
        new = monomial.monomial.fromGenerator(self)
        return new + other

    def __sub__(self,other):
        new = monomial.monomial.fromGenerator(self)
        return new - other

    def __mul__(self,other):
        new = monomial.monomial.fromGenerator(self)
        return new * other


if __name__ == '__main__':
    x = generator("x",1)
    y = generator("y",1000)
    #z = generator("", 2000)

    print x.toLatex()
    print x

