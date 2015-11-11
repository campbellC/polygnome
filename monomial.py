import abstractPolynomial
import generator
from coefficient import coefficient
import algebra
import polynomial

class monomial(abstractPolynomial.abstractPolynomial):
    """
    File: monomial.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A monomial is basically a coefficient and a tuple of generators.
    The coefficient can change if you call sort, but otherwise it is immutable.
    """
    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################
    def __init__(self, coeff=None, generators=None, alg=None):
        if coeff is None:
            coeff = coefficient()
        if generators is None:
            generators = ()

        assert isinstance(alg,algebra.algebra) or alg is None
        assert isinstance(coeff, coefficient)
        assert isinstance(generators, tuple)

        self.coefficient = coeff.sort()
        self.generators = generators
        self.algebra = alg

    @classmethod
    def fromNumberAndAlgebra(cls,num,alg):
        coeff = coefficient.fromNumber(num)
        cls(coeff,None, alg)

    @classmethod
    def fromGenerator(cls,gen):
        coeff = coefficient.fromNumber(1)
        return cls(coeff,(gen,),gen.algebra)

    @classmethod
    def fromCoefficientAndgenerators(cls,coeff,gens):
        assert len(gens)>0
        return cls(coeff,gens,gens[0].algebra)


    @classmethod
    def fromCoefficientAndAlgebra(cls,coeff,alg):
        return cls(coeff,None,alg)

    @classmethod
    def fromPolynomial(cls,poly):
        assert len(poly.monomials) <= 1
        if len(poly.monomials) == 0:
            return monomial.fromNumberAndAlgebra(0,poly.algebra)
        else:
            return poly.monomials[0]
    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################


    #def facSeq(self):#this will be a factorisation sequence which will return a  [[monomial-repr, position using r i.e. the left hand position! , r used as a one key dict]]
        #assert not self.coeffsFlag #TODO: make this work without this assertion
        #self.sanityCheck()
        #ret = []
        #mon = copy.deepcopy(self)
        #if self.sorted():
            #self.sanityCheck()
            #return ret
        #for i in range(0,len(mon.vs)-1):
            #if tuple(mon.vs[i:i+2]) in mon.rels:
                #t = copy.deepcopy(mon)
                #t.vs[i:i+2] = mon.rels[tuple(mon.vs[i:i+2])][:2]
                #return [[mon,i,{tuple(mon.vs[i:i+2]):mon.rels[tuple(mon.vs[i:i+2])]}]] + t.facSeq()

    def isSorted(self):
        if self.algebra is None:
            return True
        for index,i in enumerate(self.generators[:-1]):
            for relation in self.algebra:
                if relation.doesAct(i,self.generators[index+1]):
                    return False
        return True

    def sort(self):
        self.coefficient = self.coefficient.sort() # We allow coefficients to change
        if self.isSorted():
            return self

        for index,i in enumerate(self.generators[:-1]):
            for relation in self.algebra:
                if relation.doesAct(i,self.generators[index+1]):
                    if index > 0:
                        start = monomial.fromCoefficientAndgenerators(coefficient.fromNumber(1),self.generators[:index])
                    else:
                        start = coefficient.fromNumber(1)
                    middle = relation.act(i,self.generators[index+1])
                    if index != len(self.generators) - 2:
                        end = monomial.fromCoefficientAndgenerators(coefficient.fromNumber(1), self.generators[index+2:])
                    else:
                        end = coefficient.fromNumber(1)
                    newPoly = self.coefficient * start * middle * end
                    return newPoly.sort()




    def __iter__(self):
        for i in self.generators:
            yield i
    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################

    def degree(self):
        return len(self.generators)

    def isAddable(self,other):
        if self.degree() != other.degree():
            return False
        x = self.sort()
        y = other.sort()
        if x.generators == y.generators:
            return True
        else:
            return False

    def isNum(self):
        return len(self.generators) == 0

    def isZero(self):
        return self.coefficient.isZero()

    def __add__(self,other ):
        if isinstance(other,monomial):
            if self.algebra is other.algebra:
                if self.isAddable(other):
                    newCoefficient = self.coefficient + other.coefficient
                    return monomial(newCoefficient,self.generators,self.algebra)
                else:
                    return polynomial.polynomial.fromMonomials((self,other)).sort()
            else:
                return NotImplemented
        elif isinstance(other, generator.generator):
            other = monomial.fromGenerator(other)
            return self + other
        elif isinstance(other,coefficient):
           newMono = monomial.fromCoefficientAndAlgebra(coefficient,self.algebra)
           return self + newMono
        elif type(other) in [float,int]:
            newMono = monomial.fromNumberAndAlgebra(other,self.algebra)
            return self + newMono
        else:
            return NotImplemented



    def __mul__(self,other):
        if isinstance(other,monomial):
            if self.algebra is other.algebra:
                newCoeff = self.coefficient * other.coefficient
                newGenerators = self.generators + other.generators
                return monomial(newCoeff,newGenerators,self.algebra)
            else:
                return NotImplemented

        elif isinstance(other, generator.generator):
            other = monomial.fromGenerator(other)
            return self * other

        elif isinstance(other,coefficient):
            other = monomial.fromCoefficientAndAlgebra(other,self.algebra)
            return self * other

        elif type(other) in [float,int]:
            newCoefficient = coefficient.fromNumber(other)
            return self * newCoefficient

        else:
            return NotImplemented

    def __rmul__(self,other):
        if isinstance(other,generator.generator):
            other = monomial.fromGenerator(other)
            return other * self
        else:
            return self * other #this case should only hit for coefficients or numbers in which case the multiplication is commutative
    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################


    def __repr__(self):
        if self.isZero():
            return "0"
        elif self.isNum():
            return self.coefficient.__repr__()
        else:
            return self.coefficient.__repr__() + '*' + ''.join( x.__repr__() for x in self.generators)

    def toLatex(self):
        if self.isZero():
            return "0"
        elif self.isNum():
            return self.coefficient.toLatex()
        else:
            return self.coefficient.toLatex() + '*' + ''.join( x.toLatex() for x in self.generators)



if __name__ == '__main__':

    x = generator.generator("x",1)
    y = generator.generator("y",1000)
    #z = generator("", 2000)
    #import pdb; pdb.set_trace()
    print x + x







