import polygnomeObject
import coefficient


class doublyDefined(polygnomeObject.polygnomeObject):
    """
    File: doublyDefined.py
    Author: Chris Campbell
    Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A class to encapsulate elements of K3Bar
    """

    def __init__(self, leftHandRepresentation ,rightHandRepresentation):
        self.leftHandRepresentation = leftHandRepresentation
        self.rightHandRepresentation = rightHandRepresentation
        self.coefficient = coefficient.coefficient(1)

    def __repr__( self):
        answer = ''
        for i in self.leftHandRepresentation:
            answer += repr(i[0]) + '*' + repr(i[1])
        return answer

    def toLatex(self):
        answer = ''
        for i in self.leftHandRepresentation:
            answer += i[0].toLatex() + '*' + i[1].toLatex()
        return answer

    def __eq__(self,other):
        return self.leftHandRepresentation == other.leftHandRepresentation \
            and self.rightHandRepresentation == other.rightHandRepresentation

    ##############################################################################
    ######  CODE TO MAKE THIS USEABLE IN TENSOR PRODUCTS
    ##############################################################################

    def clean(self):
        return self

    def isZero(self):
        return False

    def __iter__(self):
        yield self

    def withCoefficientOf1(self):
        return self
