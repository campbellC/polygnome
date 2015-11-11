import abstractPolynomial
import monomial
import coefficient
import algebra
import generator

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

    def __init__(self,monomials=None,alg=None):
        if monomials is None:
            monomials = tuple()
        assert isinstance(monomials,tuple)
        assert isinstance(alg,algebra.algebra) or alg is None
        self.monomials = monomials
        self.algebra = alg

    @classmethod
    def fromMonomials(cls,monomials):
        assert len(monomials)>0
        return cls(monomials, monomials[0].algebra)

    @classmethod
    def fromMonomial(cls,mono):
        assert isinstance(mono, monomial.monomial)
        return cls((mono,),mono.algebra)

    @classmethod
    def fromGenerator(cls,gen):
        assert isinstance(gen,generator.generator)
        return polynomial.fromMonomial(monomial.fromGenerator(gen))

    @classmethod
    def fromNumberAndAlgebra(cls,num,alg=None):
        mono = monomial.fromNumberAndAlgebra(num,alg)
        return polynomial.fromMonomial(mono)

    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################
    def __iter__(self):
        for i in self.monomials:
            yield i

    def isSorted(self):
        for i in self:
            if not i.isSorted():
                return False
        for inum,i in enumerate(self):
            for jnum,j in enumerate(self):
                if jnum == inum:
                    continue

                if i.isAddable(j):
                    return False

        return True

    def sort(self): #We first check if already sorted. Then we build a new array of monomials with all of the sorted monomials together (with no duplicates). Then we remove any 0 coefficient monomials.
        if self.isSorted():
            return self
        newMonos = []
        for oldMono in self:
            newMono = oldMono.sort() # having this here is more efficient since isAddable will sort it's inputs every time it is called
            for index,otherMono in enumerate(newMonos):
                if newMono.isAddable(otherMono):
                    newMonos[index] = newMono + otherMono
                    break
            else:
                newMonos.append(newMono) # this will only happen if this sequence of generators has not been seen before

        monosWithoutZeroes = []
        for i in newMonos:
            if i.isZero():
                continue
            else:
                monosWithoutZeroes.append(i)
        if len(monosWithoutZeroes) > 0:
            return polynomial.fromMonomials(tuple(newMonos))
        else:
            return polynomial.fromNumberAndAlgebra(0,self.algebra)




    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################

    def isZero(self):
        other = self.sort()
        for i in other.monomials:
            if not i.isZero():
                return False
        return True

    def __mul__(self,other):
        if len(self.monomials) == 0:
            return self
        if len(other.monomials) == 0:
            return other
        # From here on we know length of monomials > 0
        if isinstance(other,monomial.monomial) or (type(other) in [float,int]) or isinstance(other,coefficient.coefficient):
            newMonos = []
            for i in self.monomials:
                newMonos.append(i * other)
            return polynomial.fromMonomials(tuple(newMonos))

        if isinstance(other,polynomial):
            newMonos = []
            for mono1 in self.monomials:
                for mono2 in other.monomials:
                    newMonos.append(mono1 * mono2)
            return polynomial.fromMonomials(tuple(newMonos))

    def __rmul__(self,other):
        if isinstance(other,monomial.monomial):
            other = polynomial.fromMonomial(other)
            return other * self
        elif (type(other) in [float,int]) or isinstance(other,coefficient.coefficient):
            return self * other
        else:
            return NotImplemented

    def __add__(self,other):
        if isinstance(other,polynomial):
            newMonos = self.monomials + other.monomials
            return polynomial.fromMonomials(newMonos)

        elif isinstance(other,monomial.monomial):
            other = polynomial.fromMonomial(other)
            return self + other

        elif isinstance(other,coefficient.coefficient):
           other = monomial.fromCoefficientAndAlgebra(other,self.algebra)
           return self + other

        elif isinstance(other, generator.generator):
            other = monomial.fromGenerator(other)
            return self + other

        elif type(other) in [float,int]:
            other = coefficient.fromNumber(other)
            return self + other

        else:
            return NotImplemented

    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################

    def __repr__(self):
        if self.isZero():
            return "0"
        return "+".join(x.__repr__() for x in self if not x.isZero())

    def toLatex(self):
        if self.isZero():
            return "0"
        return "+".join(x.toLatex() for x in self if not x.isZero())

if __name__ == '__main__':

    x = generator.generator("x",1)
    y = generator.generator("y",1000)
    #z = generator("", 2000)
    import pdb; pdb.set_trace()
    print 13 * x * y * 13 + x * y * y * y

