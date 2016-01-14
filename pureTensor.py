import abstractTensor
import tensor
import coefficient
import monomial #TODO: remove this ugly breaking of encapsulation
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
        if type(monomials) not in [list,tuple]:
            monomials = (monomials,)
        monomials= tuple(monomials)
        self.coefficient = coeff
        index = 0
        while index < len(monomials):
            if type(monomials[index]) in [coefficient.coefficient,int,float]:
                monomials = monomials[:index] + (monomial.monomial(monomials[index]),) + monomials[index+1:]
            index +=1
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
        if self.isZero() or other.isZero():
            return True
        else:
            return self.monomials == other.monomials

    def __add__(self,other ):
        if other == 0:
            return self
        new1 = self.clean()
        other = other.clean()
        if isinstance(other,pureTensor):
            if new1.isAddable(other):
                if self.isZero():
                    return other
                else:
                    newCoefficient = new1.coefficient + other.coefficient
                    return pureTensor(self.monomials,newCoefficient)
            else:
                return tensor.tensor((new1,other))
        else:
            return NotImplemented

    def __mul__(self,other):
        if self.isZero():
            return self
        newMonos = self.monomials[:-1] + (self.monomials[-1] * other,)
        return pureTensor(newMonos,self.coefficient).clean()

    def __rmul__(self,other):
        if self.isZero():
            return self
        newMonos = (other * self.monomials[0],) + self.monomials[1:]
        return pureTensor(newMonos,self.coefficient).clean()

    def degree(self):
        return reduce(lambda x,y: x+ y, self.monomials)

    def tensorProduct(self,other):
        if not isinstance(other, pureTensor):
            other = pureTensor( (other,) )
        return pureTensor(self.monomials + other.monomials, self.coefficient * other.coefficient)

    def subTensor(self,a,b):
        assert 0 <= a<= len(self)
        assert a <= b<= len(self)
        new = self.clean().monomials[a:b]
        return pureTensor(new)

    def __getitem__(self,index):
        return self.monomials[index]

    def __len__(self):
        return len(self.monomials)
    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################


    def __repr__(self): # TODO: add the +1 -1 stuff here.
        if self.isZero():
            return "0"
        else:
            if self.coefficient == -1:
                return '-' + '|'.join([repr(x) for x in self.monomials])
            elif self.coefficient == 1:
                return '|'.join([repr(x) for x in self.monomials])
            else:
                return repr(self.coefficient) + '*' + '|'.join([repr(x) for x in self.monomials])

    def toLatex(self):
        if self.isZero():
            return "0"
        else:
            coefficientJoiner = '*'
            if self.coefficient == -1:
                coefficientJoiner = ''
            return self.coefficient.toLatex() + coefficientJoiner +'('+ \
                '|'.join([i.toLatex() for i in self.monomials])+ ')'

