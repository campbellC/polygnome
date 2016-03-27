import arithmeticInterface
import composite

class vector(arithmeticInterface.arithmeticInterface):
    """
    File: vector.py
    Author: Chris Campbell
    Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/campbellC
    Description: A vector class for vectors of abstractPolynomials.
    """
    def __init__(self,components):
        components = tuple(components)
        assert isinstance(components, tuple)
        self.components = components

    def clean(self):
        newComponents = [x.clean() for x in self.components]
        return vector(tuple(newComponents))

    def __mul__(self,other):
        newComponents = []
        for i in self.components:
            newComponents.append(i * other)
        return vector(newComponents)

    def __add__(self,other):
        assert len(self) == len(other)
        newComponents = []
        for index, i in enumerate(self.components):
            newComponents.append(other.components[index] + i)
        return vector(newComponents)

    def __len__(self):
        return len(self.components)

    def __getitem__(self,index):
        if index > len(self):
            raise IndexError
        return self.components[index]

    def isZero(self):
        for i in self:
            if not i.isZero():
                return False
        else:
            return True

    def reduceWithRespectTo(self,alg):
        newComponents = []
        for poly in self:
            newComponents.append(alg.reduce(poly))
        return vector(newComponents)

    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################

    def __repr__(self):
        return '(' + ','.join([repr(x) for x in self.components]) + ')'

    def toLatex(self):
        return '\\left( \\begin{array}{c} \n' +\
                '\\\\ \n'.join([x.toLatex() for x in self.components]) +\
                '\n \\end{array}\\right)'

