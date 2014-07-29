import pureTensor
import copy
import monomial
import polynomial
import coefficient

class tensor():
    """a list of pure tensors """
    
    def __init__(self,ps = []):
        self.ps = copy.deepcopy(ps)
        self.sanityCheck()
    
    def isZero(self):
        self.sort()
        ret = True
        for i in self.ps:
            ret = ret and i.isZero()
        return ret
    
    def hasZeroTerms(self):
        self.sort()
        for i in self.ps:
            if i.isZero():
                return True
        return False
    ##########################################################################################################################################################
    ##################################################################SORTING METHODS ##################################################################
    ##########################################################################################################################################################
    def sorted(self):
        self.sanityCheck()
        for i in self.ps:
            if not i.sorted():
                self.sanityCheck()
                return False
        for i in self.ps:
            for j in self.ps:
                if i is j:
                    continue
                if i.addable(j):
                    return False
        self.sanityCheck()
        return True
    
    def sort(self):
        self.sanityCheck()
        if self.sorted():
            return
        for i in self.ps:
            i.sort()
        while not self.sorted():
            flag = False
            for i in self.ps:  
                if flag:
                    break
                for j in self.ps:
                    if i is j:
                        continue
                    if i.addable(j):
                        self.ps = [z for z in self.ps if (not z is i) and (not z is j) ]
                        self.ps.append(i+j)
                        flag = True
                        break
        self.deleteZeroTerms()
        self.sanityCheck()
    
    def deleteZeroTerms(self):
        self.sanityCheck()
        if not self.hasZeroTerms():
            return
        else:
            for i in range(0,len(self.ps)):
                if self.ps[i].isZero():
                    self.ps = self.ps[:i]+self.ps[i+1:]
                    break
            self.deleteZeroTerms()

    
    ##########################################################################################################################################################
    ################################################################## __methods__ ##################################################################
    ##########################################################################################################################################################
    def __repr__(self):
        if self.isZero():
            return "0"
        return "+".join(x.__repr__() for x in self.ps)
    
    def __add__(self,other):
        self.sanityCheck()
        ret = copy.deepcopy(self)
        if isinstance(other,tensor):
            other.sanityCheck()
            ret.ps += other.ps
            ret.sort()
        elif isinstance(other,pureTensor.pureTensor):
            other.sanityCheck()
            ret.ps.append(other)
            ret.sort()
        else:
            print "unwritten code in tensor +"
        return ret
    
    def __mul__(self,other):
        self.sanityCheck()
        ret = copy.deepcopy(self)
        if isinstance(other,monomial.monomial) or (type(other) in [float,int]) or isinstance(other,coefficient.coefficient):
            for i in range(0,len(ret.ps)):
                ret.ps[i] = ret.ps[i] * other
            ret.sort()
        if isinstance(other, polynomial.polynomial):
            flag = True
            for i in other.monos:
                if flag:
                    ret = ret * i
                else:
                    ret = ret + (ret * i)
            ret.sort()
        return ret
    def __sub__(self,other):
        self.sanityCheck()
        return self + (other * (-1))
    def __eq__(self,other):
        self.sanityCheck()
        x = self - other
        x.sort()
        if x.isZero():
            return True
        else:
            return False
    
    
    
##########################################################################################################################################################
    ################################################################## Debugging Code ##################################################################
    ##########################################################################################################################################################
    
    
    
    def sanityCheck(self):
        assert isinstance(self.ps,list)
        for i in self.ps:
            assert isinstance(i,pureTensor.pureTensor)
        for i in self.ps:
            for j in self.ps:
                assert i.degree() ==j.degree()
