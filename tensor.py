import abstractTensor
import pureTensor
class tensor(abstractTensor.abstractTensor):
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

    def __init__(self,pureTensors=()):
        if isinstance(pureTensors, pureTensor.pureTensor):
            pureTensors= (pureTensors,)

        assert isinstance(pureTensors,tuple)
        self.pureTensors= pureTensors


    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################
    def __iter__(self):
        for pT in self.pureTensors:
            yield pT

    def clean(self):
        self.pureTensors = map(lambda x: x.clean(),self.pureTensors)
        newpTs = []
        for index, pT in enumerate(self): #iterate through pTmials
            for j in newpTs: #check if we've seen this before
                if pT.isAddable(j):
                    break
            else: # if we haven't seen this before, take all of the pTmials with
                # the same generators and add them all together
                for index2, pT2 in enumerate(self):
                    if index >= index2:
                        continue
                    else:
                        if pT.isAddable(pT2):
                            pT = pT + pT2
                newpTs.append(pT)
        newpTs = filter(lambda x: not x.isZero(), newpTs)
        return tensor(tuple(newpTs))

    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################
    def isZero(self):
        other = self.clean()
        return len(other.pureTensors)

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




    ##########################################################################################################################################################
    ################################################################## polygnomeObject methods  ##################################################################
    ##########################################################################################################################################################
    def __repr__(self):
        if self.isZero():
            return "0"
        return "+".join(repr(x) for x in self.pureTensors)




