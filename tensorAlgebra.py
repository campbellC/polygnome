import polygnomeObject
import pureTensor
import tensor
import abstractPolynomial
class tensorAlgebra(polygnomeObject.polygnomeObject):
    """
    File: tensorAlgebra.py
    Author: Chris Campbell
    Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: This class encapsulates tensor algebras so that one can reduce
    tensors of elements from different algebras.
    """


    def __init__(self, algebras=()):
        self.algebras = tuple(algebras)

    def reduce(self,tens):
        if len(self) == 1: #If this is just an algebra
            return self[0].reduce(tens)
        newTens = tensor.tensor()
        for pure in tens:
            polys = []
            for index in range(len(pure)):
                currentAlgebra = self[index]
                polys.append(currentAlgebra.reduce(pure[index]))

            def listOfPolysToTensors(ps):
                ps = iter(ps)
                pureTensors = [pureTensor.pureTensor(mono) for mono in next(ps)]
                for poly in ps:
                    newPureTensors = []
                    for mono in poly:
                        newPureTensors.extend([x.tensorProduct(mono) for x in pureTensors])
                    pureTensors = newPureTensors
                return tensor.tensor(pureTensors)
            newTens = newTens + pure.coefficient * listOfPolysToTensors(polys)
        return newTens



    def zero(self):
        return pureTensor.pureTensor([0] * len(self))


    def __getitem__(self,index):
        return self.algebras[index]

    def __len__(self):
        return len(self.algebras)

    def __repr__(self):
        return 'A tensor algebra with algebras ' + '|'.join(repr(a) for a in self.algebras)

    def toLatex(self):
        return 'A tensor algebra with algebras ' + '|'.join(a.toLatex() for a in self.algebras)
