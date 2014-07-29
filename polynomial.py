import monomial
import copy
import coefficient
class polynomial:
    """A polynomial with it's own defined rels"""
    
    

    def __init__(self,monos=[]):
        self.monos = copy.deepcopy(monos)
        self.sanityCheck()
    
    def isZero(self):
        for i in self.monos:
            if not i.isZero():
                return False
        return True
    
    
    
    
    ##########################################################################################################################################################
    ##################################################################SORTING METHODS ##################################################################
    ##########################################################################################################################################################
    def sorted(self):
        self.sanityCheck()
        for i in self.monos:
            if not i.sorted():
                return False
        for i in self.monos:
            for j in self.monos:
                if j is i:
                    continue
                if i.safeSort()==j.safeSort():
                    self.sanityCheck()
                    return False
        self.sanityCheck()
        return True
    
    def sort(self):
        self.sanityCheck()
        if self.sorted():
            return
        flag = False
        for i in self.monos:
            i.sort()
            if flag:
                break
            for j in self.monos:
                j.sort()
                if j is i:
                    continue
                if i.safeSort()==j.safeSort():
                    self.monos = [z for z in self.monos if (not z is i) and (not z is j) ]
                    self.monos.append(i+j)
                    flag = True
                    break
        self.sanityCheck() 
        self.sort() 
    
    ##########################################################################################################################################################
    ################################################################## __methods__ ##################################################################
    ##########################################################################################################################################################
    
    def __repr__(self):
        self.sanityCheck()
        if self.isZero():
            return "0"
        return "+".join(x.__repr__() for x in self.monos if not x.isZero())

    def __mul__(self,other):
        self.sanityCheck()
        ret = copy.deepcopy(self)
        if isinstance(other,monomial.monomial) or (type(other) in [float,int]) or isinstance(other,coefficient.coefficient):
            for i in range(0,len(self.monos)):
                ret.monos[i] = ret.monos[i] * other
        if isinstance(other,polynomial):
            flag = True

            for i in other.monos:
                if flag:
                    ret = ret * i
                    flag = False
                else:
                    ret = ret + (ret * i)
        self.sanityCheck()
        return ret
    
    def __add__(self,other):
        self.sanityCheck()
        ret = copy.deepcopy(self)
        if isinstance(other,monomial.monomial):
            ret.monos.append(other)
        if isinstance(other,polynomial):
            for i in other.monos:
                ret = ret + i
        ret.sort()
        self.sanityCheck()
        return ret
    def __sub__(self,other):
        self.sanityCheck()
        return self + (other * (-1))
    ##########################################################################################################################################################
    ################################################################## Debugging Code ##################################################################
    ##########################################################################################################################################################
 
    def sanityCheck(self):
        assert isinstance(self.monos,list)
        for i in self.monos:
            assert isinstance(i,monomial.monomial)
def main():
    print "ello ello ello"
    
if __name__ == '__main__':
    main()
