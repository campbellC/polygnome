import polygnomeObject
import coefficient
import algebra

class reductionFunction(polygnomeObject.polygnomeObject):
    """
    File: reductionFunction.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A linear map on abstractPolynomials that depends on a relation
    and two submonomials left and right. If a monomial matches exactly these left
    and right submonomials with the left hand side of the relation then it returns
    the left and right wrapped around the right hand side of the relation.
    """


    def __init__(self, left, relation, right, alg = None):
		if alg is None:
			alg = left.algebra
		self.right = right
		self.relation = relation
		self.algebra = alg
		self.left = left


    def degree(self):
        return self.left.degree() + self.right.degree()+self.relation.LHS.degree()


    def __call__(self,poly):
        answer = coefficient.coefficient.fromNumber(0)
        for mono in poly:
            if self.degree() != mono.degree():
                answer = answer + mono
            elif self.left == mono.submonomial(0,self.left.degree()) \
                and self.right == mono.submonomial(self.left.degree() + 2,mono.degree())\
                and self.relation.doesAct(mono.submonomial(self.left.degree(),self.left.degree()+2)):
                    answer = answer + mono.coefficient * self.left * self.algebra.canonicalProjection(self.relation.RHS) * self.right
            else:
                answer = answer + mono
        return answer.clean()
    
    def __repr__(self):
		return "Reduction for " +repr(self.left)+repr(self.relation)+repr(self.right)

    def toLatex(self): 
		return "Reduction for " +self.left.toLatex()+self.relation.toLatex()+self.right.toLatex()

