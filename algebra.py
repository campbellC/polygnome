import polygnomeObject
import relation
import generator

class algebra(polygnomeObject.polygnomeObject):
    """
    File: algebra.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: An algebra is basically a container for generators and relations, so that polynomials know where they live.
    """
    def __init__(self,gens,rels=[]):
        self.generators = gens
        self.relations = rels
        self.sanityCheck()


    def __repr__(self):
        return "Algebra with generators " + self.generators.__repr__() + " subject to relations " + self.relations.__repr__()

    def toLatex(self):
        return "Algebra with generators $" + "$,$".join([i.toLatex() for i in self.generators])\
            + "$ subject to relations $" + "$,$".join([i.toLatex() for i in self.relations]) + "$"


    def sanityCheck(self):
        assert type(self.generators) is list
        assert len(self.generators) > 0
        for i in self.generators:
            assert isinstance(i,generator.generator)
        assert type(self.relations) is list
        for i in self.relations:
            assert isinstance(i,relation.relation)

if __name__ == '__main__':
    x = generator.generator(x)
    y = generator.generator(y)
    r = relation
