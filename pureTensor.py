import abstractTensor
import tensor
import coefficient

class pureTensor(abstractTensor.abstractTensor):
    """
    File: pureTensor.py
    Author: Chris Campbell
    Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A pureTensor is simply a pure tensor element in a tensor product.
    """


    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################
    def __init__(self, monomials=(), coeff=coefficient.coefficient(1)):

        self.coefficient = coeff
        for i in monomials:
            self.coefficient = self.coefficient * i.coefficient

        self.monomials = tuple( [x.withCoefficientOf1() for x in monomials])

    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################
    def isZero(self):
        if len(self.monomials) == 0:
            return True

        for mono in self.monomials:
            if mono.isZero():
                return True
        else:
            return False

    def clean(self):
        newCoefficient = reduce(lambda x,y: x * y, [x.coefficient for x in self.monomials], self.coefficient)
        if newCoefficient.isZero():
            return pureTensor()

        newMonos = [x.clean() for x in self.monomials]
        return pureTensor(tuple(newMonos), newCoefficient)

    def __iter__(self):
        yield self

    def isAddable(self,other):
        new1 = self.clean()
        new2 = other.clean()

        if new1.isZero() or new2.isZero():
            return True


        else:
            return new1.monomials == new2.monomials

    def __add__(self,other ):
        new1 = self.clean()
        other = other.clean()
        if isinstance(other,pureTensor):
            if new1.isAddable(other):
                newCoefficient = new1.coefficient + other.coefficient
                return pureTensor(self.monomials,newCoefficient)
            else:
                return tensor.tensor((new1,other))
        else:
            return NotImplemented

    def __mul__(self,other):
        if self.isZero():
            return self
        newMonos = self.monomials[:-1] + self.monomials[-1] * other
        return pureTensor(newMonos)

    def degree(self):
        return reduce(lambda x,y: x+ y, self.monomials)

    def tensorProduct(self,other):
        assert isinstance(other, pureTensor)
        return pureTensor(self.monomials + other.monomials, self.coefficient * other.coefficient)
    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################


    def __repr__(self): # TODO: add the +1 -1 stuff here.
        if self.isZero():
            return "0"
        else:
            coefficientJoiner = '*'
            if self.coefficient == -1:
                coefficientJoiner = ''
            return repr(self.coefficient) + coefficientJoiner + '|'.join([repr(x) for x in self.monomials])

    def toLatex(self):
        if self.isZero():
            return "0"
        else:
            coefficientJoiner = '*'
            if self.coefficient == -1:
                coefficientJoiner = ''
            return self.coefficient.toLatex() + coefficientJoiner +'('+ \
                '|'.join([i.toLatex() for i in self.monomials])+ ')'

