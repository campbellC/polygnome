from collections import namedtuple
import polygnomeObject

class relation(namedtuple('relation',['leadingMonomial','lowerOrderTerms']),
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
    def __repr__( self):
        return repr(self.leadingMonomial - self.lowerOrderTerms)

    def toLatex(self):
        return (self.leadingMonomial - self.lowerOrderTerms).toLatex()

    def doesAct(self,poly):
        return poly == self.leadingMonomial

    def degree(self):
        return self.leadingMonomial.degree()
