import copy


class coefficient():
    """coefficient of monomial or pure tensor"""
    def __init__(self,coeffs = {"" : 1}):
        self.coeffs = copy.deepcopy(coeffs)
        self.sanityCheck()
    
    def sort(self): #WARNING - assumes length one variables in the base ring!
        newCoeffs = {}
        for key in self.coeffs:
            newkey = ''.join(sorted(key))
            if newkey in newCoeffs:
                newCoeffs[newkey] += self.coeffs[key]
            else:
                newCoeffs[newkey] = self.coeffs[key]
        newCoeffs = {key : value for key, value in newCoeffs.items() if value != 0}
        if newCoeffs == {}:
            newCoeffs = {'':0}
        self.coeffs = newCoeffs
        self.sanityCheck()
            
    
    def isZero(self):
        for i in self.coeffs:
            if self.coeffs[i] !=0:
                return False
        return True
    
    
    def sanityCheck(self):
        assert isinstance(self.coeffs,dict)
        for i in self.coeffs.keys():
            assert isinstance(i,str)
        for i in self.coeffs.values():
            assert type(i) in [float,int]
    
    def __eq__(self,other):
        for i in self.coeffs:
            if not (i in other.coeffs) or other.coeffs[i]!=self.coeffs[i]:
                return False
        for j in other.coeffs:
            if not (j in other.coeffs):
                return False
        return True
        
    def __repr__(self):
        self.sanityCheck()
        if self.isZero():
            ret = "0"
        else:
            bracketFlag = False
            if len(self.coeffs) == 1:
                bracketFlag = True
                ret = ""
            else:
                ret = "("
            ret += "+".join(str(self.coeffs[i])+i if (self.coeffs[i]!=1 and self.coeffs[i]!=0 and self.coeffs[i]!=-1)
                                                    else i if (self.coeffs[i] == 1 and i != "")
                                                    else str(1) if self.coeffs[i] == 1
                                                    else "-"+i if self.coeffs[i]==-1
                                                    else "0" for i in self.coeffs)
            if not bracketFlag:
                ret += ")"
        return ret
    
    def __add__(self,other ):
        if isinstance(other,coefficient):
            self.sanityCheck()
            other.sanityCheck()
            ret = copy.deepcopy(self)
            for i in other.coeffs:
                if i in self.coeffs:
                    ret.coeffs[i] = self.coeffs[i]+other.coeffs[i]
                else:
                    ret.coeffs[i]=other.coeffs[i]
            ret.sort()
            return ret
                
    def times(self,other):
        nDict = {}    
        if isinstance(other,coefficient):
            self.sanityCheck()
            other.sanityCheck()
            for i in self.coeffs:
                for j in other.coeffs:
                    if i+j in nDict:
                        nDict[i+j] += self.coeffs[i]*other.coeffs[j]
                    else:
                        nDict[i+j]  = self.coeffs[i]*other.coeffs[j]
        if type(other) in [float,int]:
            for i in self.coeffs:
                nDict[i] = self.coeffs[i]*other
        if type(other) in [str]:
            for i in self.coeffs:
                nDict[i+other] = self.coeffs[i]
        return coefficient(nDict)
        
    def __sub__(self,other):
        self.sanityCheck()
        return self + (other * (-1))   
    
    def __mul__(self,other):
        return self.times(other)
