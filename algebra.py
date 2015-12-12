import polygnomeObject
import relation
import reductionFunction
class algebra(polygnomeObject.polygnomeObject):
    """
    File: algebra.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: An algebra is basically a container for relations, so that polynomials know where they live.
    """
    def __init__(self,relations=None):
        if relations is None:
            relations =()
        if isinstance(relations,relation.relation):
            relations = (relations,)
        assert isinstance(relations,tuple)
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
        """Test is the polynomial has any monomial on which there is a relation that acts"""
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


    def canonicalProjection(self,poly):
        return poly.changeAlgebra(self)




if __name__ == '__main__':
    pass
