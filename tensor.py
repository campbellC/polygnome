import abstractTensor
import pureTensor
import composite


class tensor(composite.composite,abstractTensor.abstractTensor):
    """
    File: tensor.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A composite class of pureTensors
    """

    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################

    def __init__(self,polynomials=()):
        pureTensors = ()
        if isinstance(polynomials, pureTensor.pureTensor):
            pureTensors = (polynomials,)
        if len(polynomials) >= 1:
            if isinstance(polynomials[0], pureTensor.pureTensor): # If this is a list of pureTensors, just conver to tuple and carry on
                pureTensors = tuple(polynomials)
            else: #Otherwise, we assume it is a list of polynomials and try and seperate into a list of pure tensors
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
        self.pureTensors = pureTensors


    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################


    def __mul__(self,other):
        if len(self) == 0:
            return self
        else:
            return tensor( map(lambda x: x * other, self))


    def __rmul__(self,other):
        if len(self) == 0:
            return self
        else:
            return tensor( map(lambda x:  other * x, self))



    def __add__(self,other):
        if other == 0:
            return self
        if isinstance(other,abstractTensor.abstractTensor):
            return composite.composite.__add__(self,other)
        else:
            return NotImplemented

    def tensorProduct(self,other):
        answer = tensor()
        for i in self:
            answer = answer + i.tensorProduct(other)
        return answer


