import polygnomeObject
import relation
import reductionFunction
import monomial
class algebra(polygnomeObject.polygnomeObject):
    """
    File: algebra.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/campbellC
    Description: An algebra stores a list of relations and can reduce words in
    the free algebra by these relations. The relations have a choice of highest monomial already.
    """
    def __init__(self,relations=()):
        if isinstance(relations,relation.relation):
            relations = (relations,)
        relations = tuple(relations)
        # If you only want one relation the following saves you having to
        # define it seperately before making the algebra.
        if len(relations) > 0 and isinstance(relations[0],tuple):
            assert len(relations[0]) == 2
            relations = map(lambda x: relation.relation( *x),relations)

        for i in relations:
            assert isinstance(i,relation.relation)
        self.relations = relations

    def zero(self):
        return monomial.monomial(0)

    def __repr__(self):
        if len(self.relations) == 0:
            return 'The free algebra'
        return "Algebra subject to relations " + repr(self.relations)

    def toLatex(self):
        if len(self.relations) == 0:
            return 'The free algebra'
        return "Algebra subject to relations $" + "$,$".join([i.toLatex() for i in self.relations]) + "$"


    def __iter__(self):
        """Iterating through an algebra simply returns the relations of that algebra"""
        for i in self.relations:
            yield i

    def doesAct(self,poly):
        """Test if the polynomial has any monomial on which there is a relation that acts"""
        for mono in poly:
            monoDegree = mono.degree()
            if monoDegree <= 1:
                continue
            for rel in self.relations:
                # For each relation we check if it applies to the monomial.
                # Firstly we check if the monomial has too low a degree
                relDegree = rel.degree()
                if monoDegree < relDegree:
                    continue

                # Secondly we iterate through the submonomials of length
                # relDegree and see if any of them are the leading monomial of
                # rel.
                for index in xrange(monoDegree - relDegree + 1):
                    if rel.doesAct(mono[index: index + relDegree]):
                        return True

        return False

    def makeReductionFunction(self, poly):
        """Only run this if you have already checked doesAct"""
        for mono in poly:
            monoDegree = mono.degree()
            if monoDegree <= 1:
                continue
            for rel in self.relations:
                # For each relation we check if it applies to the monomial.
                # Firstly we check if the monomial has too low a degree
                relDegree = rel.degree()
                if monoDegree < relDegree:
                    continue

                # Secondly we iterate through the submonomials of length
                # relDegree and see if any of them are the leading monomial of
                # rel.
                for index in xrange(monoDegree - relDegree + 1):
                    if rel.doesAct(mono[index: index + relDegree]):
                        return (reductionFunction.reductionFunction(mono[0:index],
                                                                    rel,
                                                                    mono[index + relDegree:])
                                , mono.coefficient)


    def makeReductionSequence(self,poly):
        sequence = []
        while self.doesAct(poly):
            reduction, weight = self.makeReductionFunction(poly)
            sequence.append((reduction,weight))
            poly = reduction(poly)
        return sequence

    def reductionSequenceGenerator(self,poly):
        while self.doesAct(poly):
            reduction, weight = self.makeReductionFunction(poly)
            yield (reduction, weight)
            poly = reduction(poly)


    def reduce(self,poly): # TODO: check running time on this, this is a slow way of doing iterable
        for reduction, weight in self.makeReductionSequence(poly):
            poly = reduction(poly)
        return poly


    def equivalent(self,polynomial1,polynomial2):
        return self.reduce(polynomial1) == self.reduce(polynomial2)

if __name__ == '__main__':
    pass
