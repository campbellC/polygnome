import re
import abstractPolynomial

class coefficient(abstractPolynomial.abstractPolynomial):
    """
    File: coefficient.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A coefficient is an element of a commutative ring with variables of the form <letter><number>+ (e.g. a1 + a2 could be
    stored as a coefficient but not var1).
    """
    ##############################################################################
    ######  CONSTRUCTORS
    ##############################################################################
    def __init__(self, coeffs=None):
        if coeffs is None:
            coeffs = {'' : 1}
        assert isinstance(coeffs,dict)
        self.coeffs = coeffs

    @classmethod
    def fromNumber(cls,num):
        coeffs = {"" : num}
        return cls(coeffs)

    @classmethod
    def fromString(cls,string): #very rudimentary for now only handles variables like "q" or "a1" or maybe "a2a3" nothing better though!
        coeffs = {string : 1}
        return cls(coeffs)
    ##############################################################################
    ######  SORTING METHODS
    ##############################################################################

    def _sortVars(self,variables):#this helper function sorts variables by splitting into an array using the varRE regex and then sorting the array and joining it all up again
        assert isinstance(variables, str)
        if variables == "":
            return ""
        arr = []
        while variables != "":
            m = re.match(r"([a-zA-Z][\d]*)+",variables)
            arr.append(m.group(1))
            variables = variables[:-len(m.group(1))]
        variables = "".join(sorted(arr))
        return variables

    def isSorted(self):
        for i in self.coeffs:
            if i != self._sortVars(i):
                return False
        return True

    def sort(self):
        newCoeffs = {}

        #WARNING - assumes length one variables in the base ring or length one plus number, like a1 b2 x9!

        for key in self.coeffs:
            newkey = self._sortVars(key)
            if newkey in newCoeffs:
                newCoeffs[newkey] += self.coeffs[key]
            else:
                newCoeffs[newkey] = self.coeffs[key]
        newCoeffs = {key : value for key, value in newCoeffs.items() if value != 0}
        if newCoeffs == {}:
            newCoeffs = {'':0}
        return coefficient(newCoeffs)

    ##############################################################################
    ######  MATHEMATICAL METHODS
    ##############################################################################
    def isNum(self):
        for i in self.coeffs:
            if i != "":
                if self.coeffs[i] != 0:
                    return False
        return True

    def isZero(self):
        for i in self.coeffs:
            if self.coeffs[i] !=0:
                return False
        return True

    def __add__(self,other ):
        if isinstance(other,coefficient):
            newCoeffs = {}
            for i in other.coeffs:
                if i in self.coeffs:
                   newCoeffs[i] = self.coeffs[i]+other.coeffs[i]
                else:
                    newCoeffs[i]=other.coeffs[i]
            for i in self.coeffs:
                if i in other.coeffs:
                    continue
                else:
                    newCoeffs[i] = self.coeffs[i]
            newCoefficient = coefficient(newCoeffs)
            return newCoefficient.sort()
        elif type(other) in [float,int]:
            newCoefficient = coefficient.fromNumber(other)
            return self + newCoefficient
        else:
            return NotImplemented


    def __mul__(self,other):
        if isinstance(other,coefficient):
            newCoeffs = {}
            for i in self.coeffs:
                for j in other.coeffs:
                    if i+j in newCoeffs:
                        newCoeffs[i+j] += self.coeffs[i]*other.coeffs[j]
                    else:
                        newCoeffs[i+j] = self.coeffs[i]*other.coeffs[j]
            newCoefficient = coefficient(newCoeffs)
            return newCoefficient.sort()
        elif type(other) in [float,int]:
            newCoefficient = coefficient.fromNumber(other)
            return self * newCoefficient
        else:
            return NotImplemented

    def __rmul__(self,other):
        if type(other) in [float,int]:
            return self * other
        else:
            return NotImplemented


    ##############################################################################
    ######  PRINTING AND TYPING
    ##############################################################################


    def __repr__(self):
        if self.isZero():
            ret = "0"
        else:
            bracketFlag = False
            if len(self.coeffs) == 1:
                bracketFlag = True
                ret = ""
            else:
                ret = "("
            ret += "+".join( str(self.coeffs[i])+i if (self.coeffs[i]!=1 and self.coeffs[i]!=0 and self.coeffs[i]!=-1)\
                            else i if (self.coeffs[i] == 1 and i != "")\
                            else str(1) if self.coeffs[i] == 1\
                            else "-"+i if self.coeffs[i] == -1\
                            else "0" for i in self.coeffs)

            if not bracketFlag:
                ret += ")"
        return ret

    def toLatex(self):
        string = self.__repr__()
        varWithNumRE = re.compile(r"([a-zA-Z])(\d)")
        return re.sub(varWithNumRE, r'\1_{\2}', string)




if __name__ == '__main__':
    q = coefficient.fromString('q')
    a1 = coefficient.fromString('a1')
    zero = coefficient.fromNumber(0)

    print q + zero
    print q * zero
    print q * 1
    print q + a1
    print (q+ a1).toLatex()
