import abstractAlgebra
import relation
import reductionFunction
from collections import namedtuple


# import polygnomeObject
# import abstractPolynomial


    # def doesAct(self,poly): #some iterable containing symbols
        # poly = poly.changeAlgebra(None)
        # return (poly - self.LHS).isZero()

    # def act(self,poly):
        # if self.doesAct(poly):
            # return self.RHS
        # else:
            # return poly

class algebra(abstractAlgebra.abstractAlgebra):
    """
    File: algebra.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: An algebra stores a list of relations and can reduce words in
    the free algebra by these relations. The relations have a choice of highest monomial already.
    """
    def __init__(self,relations=()):
        if isinstance(relations,relation.relation):
            relations = (relations,)

        if not isinstance(relations,tuple):
            raise TypeError("Expected relations")
        if len(relations) > 0 and isinstance(relations[0],tuple):
            assert len(relations[0]) == 2
            relations = map(lambda x: relation.relation( *x),relations)

        for i in relations:
            assert isinstance(i,relation.relation)
        self.relations = relations

    def __repr__(self):
        return "Algebra subject to relations " + repr(self.relations)

    def toLatex(self):
        return "Algebra subject to relations $" + "$,$".join([i.toLatex() for i in self.relations]) + "$"


    def __iter__(self):
        """Iterating through an algebra simply returns the relations of that algebra"""
        for i in self.relations:
            yield i

    def doesAct(self,poly): #Assumes degree 2 relations
        """Test if the polynomial has any monomial on which there is a relation that acts"""
        for mono in poly:
            n = mono.degree()
            if n <= 1:
                continue
            for a in xrange(n-1):
                for i in self.relations:
                    if i.doesAct(mono.submonomial(a,a+2)):
                        return True
        return False

    def makeReductionFunction(self,poly):
        """Only run this if you have already checked doesAct"""
        for mono in poly:
            n = mono.degree()
            if n <= 1:
                continue
            for a in xrange(n-1):
                for i in self.relations:
                    if i.doesAct(mono.submonomial(a,a+2)):
                        return reductionFunction.reductionFunction(mono.submonomial(0,a),i,mono.submonomial(a+2,n))


    def makeReductionSequence(self,poly):
        sequence = []
        while self.doesAct(poly):
            reduction = self.makeReductionFunction(poly)
            sequence.append(reduction)
            poly = reduction(poly)
        return sequence

    def reduce(self,poly): # TODO: check running time on this, this is a slow way of doing iterable
        for i in self.makeReductionSequence(poly):
            poly = i(poly)
        return poly


if __name__ == '__main__':
    pass
