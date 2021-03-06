from abc import ABCMeta, abstractmethod
import polygnomeObject
class composite(polygnomeObject.polygnomeObject):
    __metaclass__ = ABCMeta
    """
    File: composite.py
    Author: Chris Campbell
    Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/campbellC
    Description: This class abstracts the fact that tensor is to pure tensor as polynomial is to monomial.
    """

    def __init__(self, components=()):
        self.components = components

    def __iter__(self):
        for component in self.components:
            yield component

    def isZero(self):
        other = self.clean()
        return len(other.components) == 0


    def clean(self):
        currentComponents = map(lambda x: x.clean(),self.components)
        newComponents = []
        for index, component in enumerate(currentComponents): #iterate through components
            for j in newComponents: #check if we've seen this before
                if component.isAddable(j):
                    break
            else: # if we haven't seen this before, take all of the componentmials with
                # the same generators and add them all together
                for index2, component2 in enumerate(currentComponents):
                    if index >= index2:
                        continue
                    else:
                        if component.isAddable(component2):
                            component = component + component2
                newComponents.append(component)
        newComponents = filter(lambda x: not x.isZero(), newComponents)
        return type(self)(tuple(newComponents))

    def __len__(self):
        return len(self.components)

    def __getitem__(self,index):
        return self.components[index]
    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################

    def __add__(self,other):
        newComponents = [x for x in self] + [x for x in other]
        return (type(self)(newComponents)).clean()

    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################

    def __repr__(self):
        if self.isZero():
            return '0'
        return "+".join(repr(x) for x in self if not x.isZero())

    def toLatex(self):
        if self.isZero():
            return "0"
        return "+".join(x.toLatex() for x in self if not x.isZero())
