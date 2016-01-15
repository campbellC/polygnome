from collections import namedtuple
import polygnomeObject
import coefficient

relationClass = namedtuple('relation',['leadingMonomial','lowerOrderTerms'])
class relation(relationClass,
               polygnomeObject.polygnomeObject): # type definition: relation is
                                                #a tuple with the leading monomial
                                                # and the lower terms in the
                                                # reduction hierarchy
    """
    File: relation.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description:A relation is a tuple with the leadingMonomial and lowerOrderTerms.
    """
    def __init__(self,*args,**kwargs):
        relationClass.__init__(self,args,kwargs)
        self.coefficient = coefficient.coefficient(1)

    def __repr__( self):
        return '(' + repr(self.leadingMonomial - self.lowerOrderTerms) + ')'

    def toLatex(self):
        return '(' + (self.leadingMonomial - self.lowerOrderTerms).toLatex() + ')'

    def doesAct(self,poly):
        return poly == self.leadingMonomial

    def degree(self):
        return self.leadingMonomial.degree()

    def __eq__(self,other):
        return self.leadingMonomial == other.leadingMonomial and self.lowerOrderTerms == other.lowerOrderTerms

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
