import polygnomeObject
import relation

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
        assert isinstance(relations,tuple)
        for i in relations:
            assert isinstance(i,relation.relation)
        self.relations = relations

    def __repr__(self):
        return "Algebra subject to relations " + self.relations.__repr__()

    def toLatex(self):
        return "Algebra subject to relations $" + "$,$".join([i.toLatex() for i in self.relations]) + "$"


    def __iter__(self):
        """Iterating through an algebra simply returns the relations of that algebra"""
        for i in self.relations:
            yield i


if __name__ == '__main__':
    pass
