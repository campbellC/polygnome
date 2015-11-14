import abstractPolynomial
import generator
import coefficient
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
            coeff = coefficient.coefficient()
        if generators is None:
            generators = ()

        assert isinstance(alg,algebra.algebra) or alg is None
        assert isinstance(coeff, coefficient.coefficient)
        assert isinstance(generators, tuple)

        self.coefficient = coeff.sort()
        self.generators = generators
        self.algebra = alg

    @classmethod
    def fromNumberAndAlgebra(cls,num,alg):
        coeff = coefficient.coefficient.fromNumber(num)
        cls(coeff,None, alg)

    @classmethod
    def fromGenerator(cls,gen):
        coeff = coefficient.coefficient.fromNumber(1)
        return cls(coeff,(gen,),gen.algebra)

    @classmethod
    def fromCoefficientAndGenerators(cls,coeff,gens):
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



    def changeAlgebra(self,alg):
        newGens = [x.changeAlgebra(alg) for x in self.generators]
        return monomial(self.coefficient,newGens,alg)

    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################
    def clean(self):
        return monomial(self.coefficient.sort(),self.generators,self.algebra)

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


    def submonomial(self,a,b): #returns the monomial from position a to position b (right hand open). e.g. xy._submonomial(0,1) = x. sets coefficient to one
        assert 0 < a < len(self.generators)
        assert a <= b <= len(self.generators)
        newGens = self.generators[a:b]
        return monomial(coefficient.coefficient.fromNumber(1),newGens,self.algebra)




    #def sort(self):
        #self.coefficient = self.coefficient.sort() # We allow coefficients to change
        #if self.isSorted():
            #return self

        #for index,i in enumerate(self.generators[:-1]):
            #for relation in self.algebra:
                #if relation.doesAct(i,self.generators[index+1]):
                    #if index > 0:
                        #start = monomial.fromCoefficientAndgenerators(coefficient.coefficient.fromNumber(1),self.generators[:index])
                    #else:
                        #start = coefficient.coefficient.fromNumber(1)
                    #middle = relation.act(i,self.generators[index+1])
                    #if index != len(self.generators) - 2:
                        #end = monomial.fromCoefficientAndgenerators(coefficient.coefficient.fromNumber(1), self.generators[index+2:])
                    #else:
                        #end = coefficient.coefficient.fromNumber(1)
                    #newPoly = self.coefficient * start * middle * end
                    #return newPoly.sort()




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
        elif isinstance(other,coefficient.coefficient):
           newMono = monomial.fromCoefficientAndAlgebra(other,self.algebra)
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

        elif isinstance(other,coefficient.coefficient):
            other = monomial.fromCoefficientAndAlgebra(other,self.algebra)
            return self * other

        elif type(other) in [float,int]:
            newCoefficient = coefficient.coefficient.fromNumber(other)
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
    pass






