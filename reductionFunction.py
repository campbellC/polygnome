import polygnomeObject
import coefficient
import algebra
from collections import namedtuple

class reductionFunction(namedtuple('reductionFunction', ['leftMonomial','relation','rightMonomial']), polygnomeObject.polygnomeObject):
    """
    File: reductionFunction.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/campbellC
    Description: A linear map on abstractPolynomials that depends on a relation
    and two submonomials left and rightMonomial. If a monomial matches exactly these left
    and right submonomials with the left hand side of the relation then it returns
    the left and right wrapped around the right hand side of the relation.
    """



    def degree(self):
        return self.leftMonomial.degree() + self.rightMonomial.degree()+self.relation.degree()


    def __call__(self,poly):
        answer = coefficient.coefficient(0)
        for mono in poly:
            if self.degree() != mono.degree():
                answer = answer + mono
#TODO: check impact of this choice of order of condition checks on running time
            elif self.leftMonomial == mono.submonomial(0,self.leftMonomial.degree()) \
                and self.rightMonomial == mono.submonomial(self.leftMonomial.degree() + self.relation.degree(),mono.degree())\
                and self.relation.doesAct(mono.submonomial(self.leftMonomial.degree(),self.leftMonomial.degree()+self.relation.degree())):
                    answer = answer + mono.coefficient * self.leftMonomial * self.relation.lowerOrderTerms * self.rightMonomial
            else:
                answer = answer + mono
        return answer.clean()

    def __repr__(self):
        return repr(self.leftMonomial) +"("+repr(self.relation)+")"+repr(self.rightMonomial)

    def toLatex(self):
        return self.leftMonomial.toLatex() +"("+self.relation.toLatex()+")"+self.rightMonomial.toLatex()

