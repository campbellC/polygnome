import abstractTensor
import pureTensor
import composite


class tensor(abstractTensor.abstractTensor,composite.composite):
    """
    File: tensor.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A composite class of pureTensors
    """
    # TODO: This is almost exactly the same code as polynomial. Need to abstract
    # this relationship

    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################

    def __init__(self,polynomials=()):
        pureTensors = ()
        if isinstance(polynomials, pureTensor.pureTensor):
            pureTensors = (polynomials,)
        if len(polynomials) >= 1:
            if isinstance(polynomials[0], pureTensor.pureTensor):
                pureTensors = tuple(polynomials)
            else:

                def pureTensorHelper(polynomials):
                    assert len(polynomials) > 0
                    for i in polynomials:
                        if i.isZero():
                            return tensor()

                    pureTensors = []
                    if len(polynomials) == 1:
                        for mono in polynomials[0]:
                            pureTensors.append(pureTensor.pureTensor( (mono,) ))
                    else:
                        tempTensors = pureTensorHelper(polynomials[1:])
                        for mono in polynomials[0]:
                            for pT in tempTensors:
                                pureTensors.append(pureTensor.pureTensor( (mono,) ).tensorProduct(pT))

                    return tuple(pureTensors)

                pureTensors = pureTensorHelper(polynomials)

        assert isinstance(pureTensors,tuple)
        composite.composite.__init__(self,pureTensors)
        self.pureTensors= pureTensors


    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################

    def clean(self):
        return self._clean(tensor)

    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################
    def __iter__(self):
        return composite.composite.__iter__(self)

    def isZero(self):
        return composite.composite.isZero(self)

    def __mul__(self,other):
        if len(self.pureTensors) == 0:
            return self
        else:
            return tensor( map(lambda x: x * other, self.pureTensors))


    def __rmul__(self,other):
        if len(self.pureTensors) == 0:
            return self
        else:
            return tensor( map(lambda x:  other * x, self.pureTensors))



    def __add__(self,other):
        if isinstance(other,tensor):
            newPTs = self.pureTensors + other.pureTensors
            return tensor(newPTs).clean()

        if isinstance(other,pureTensor.pureTensor):
            return self + tensor(other)
        else:
            return NotImplemented





    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################

    def __repr__(self):
        return composite.composite.__repr__(self)

    def toLatex(self):
        return composite.composite.toLatex(self)
