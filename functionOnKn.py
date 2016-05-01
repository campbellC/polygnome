import vector
import tensorAlgebra
import algebra
import bimoduleMapDecorator

class functionOnKn(vector.vector):
    """
    File: functionOnKn.py
    Author: Chris Campbell
    Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/campbellC
    Description: A function on Kn represented as a vector.
    """
    def __init__(self, alg, basisOfKn, images):
        self.codomain = self.algebra = alg
        self.basisOfKn = basisOfKn #This is a basis of the intersection space in the free algebra
        freeAlgebra = algebra.algebra()
        self.domain = tensorAlgebra.tensorAlgebra([alg,freeAlgebra,alg])
        vector.vector.__init__(self,images)

    def __call__(self, tensor):

        @bimoduleMapDecorator.bimoduleMapDecorator(self.domain,self.codomain)
        def helper(PT):
            index = self.basisOfKn.index(PT)
            return self[index]

        return helper(tensor)

    def __add__(self,other):
        assert isinstance(other, functionOnKn)
        return functionOnKn(self.algebra, self.basisOfKn, [a + b for a,b in zip(self.components, other.components)])

    def __mul__(self,other):
        return functionOnKn(self.algebra, self.basisOfKn, [a * other for a in self.components] )
if __name__ == '__main__':
    pass
