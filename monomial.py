import polynomial
import coefficient
import copy
import tensor
import pureTensor

class monomial:
    """A monomial is just a list of variables with a coefficient"""
    
    def __init__(self,vs = [],symbs=[],rels={},coeff = coefficient.coefficient()):
        self.symbs = copy.deepcopy(symbs)
        self.rels = copy.deepcopy(rels)
        self.coeff = copy.deepcopy(coeff)
        self.vs = copy.deepcopy(vs)
        self.sanityCheck()
    
    def degree(self):
        return len(self.vs)
    
    def isNum(self):
        return len(self.vs) == 0
    
    def isZero(self):
        return self.coeff.isZero()
    
    ##################################################################################################################
    #### Methods for sorting the monomial
    ###################################################################################################################
    def sorted(self):
        self.sanityCheck()
        for i in range(0,len(self.vs)-1):
            if tuple(self.vs[i:i+2]) in self.rels:
                self.sanityCheck()
                return False
        self.sanityCheck()
        return True
    
    def sort(self):
        self.sanityCheck()
        if self.sorted():
            return
        for i in range(0,len(self.vs)-1):
            if tuple(self.vs[i:i+2]) in self.rels:
                self.vs[i:i+2] = self.rels[tuple(self.vs[i:i+2])]
                break
        self.sanityCheck()
        self.sort()
            
    def safeSort(self):#this will output the sorted list
        self.sanityCheck()
        ret = copy.deepcopy(self)
        ret.sort()
        return ret.vs
        
    def facSeq(self):#this will be a factorisation sequence which will return a  [[monomial-repr, position using r, i.e. the left hand position! , r used as a one key dict]]
        self.sanityCheck()
        ret = []
        mon = copy.deepcopy(self)
        if self.sorted():
            self.sanityCheck()
            return ret
        for i in range(0,len(mon.vs)-1):
            if tuple(mon.vs[i:i+2]) in mon.rels:
                t = copy.deepcopy(mon)
                t.vs[i:i+2] = mon.rels[tuple(mon.vs[i:i+2])]
                return [[mon,i,{tuple(mon.vs[i:i+2]):mon.rels[tuple(mon.vs[i:i+2])]}]] + t.facSeq() 
    
                
    ##################################################################################################################
    #### __methods__ 
    ###################################################################################################################       
    
    def __eq__(self,other):
        self.sanityCheck()
        x=self-other
        x.sort()
        if x.isZero():
            return True
        else:
            return False
    
    def __repr__(self):
        self.sanityCheck()
        if self.isZero():
            return "0"
        if self.coeff.coeffs == coefficient.coefficient({"":1}).coeffs:
            if self.vs == []:
                return "1"
            return "".join(self.vs)
        elif self.coeff.coeffs == coefficient.coefficient({"":-1}).coeffs:
            return "-"+"".join(self.vs)
        else:
            return self.coeff.__repr__() +"*" + "".join(self.vs)
    
    def __add__(self,other):
        if isinstance(other,monomial):
            assert other.symbs == self.symbs
            assert other.rels==self.rels
            if self.safeSort() == other.safeSort():
                m = copy.deepcopy(self)
                m.coeff = m.coeff + other.coeff
                return m
            return polynomial.polynomial([copy.deepcopy(self),copy.deepcopy(other)])
        if isinstance(other,polynomial.polynomial):
            answer = copy.deepcopy(other)
            return answer + self
      
    def __mul__(self,other):
        self.sanityCheck()
        ret = copy.deepcopy(self)
        if isinstance(other,polynomial.polynomial):
            ret = polynomial.polynomial()
            for i in other.monos:
                ret = ret + self * i
        if isinstance(other,monomial):
            ret.vs += other.vs
            ret.coeff = ret.coeff*other.coeff
        
        if isinstance(other,pureTensor.pureTensor):
            ret = copy.deepcopy(other)
            ret.monos[0] = self * ret.monos[0]
            ret.sort()
        if isinstance(other,tensor.tensor):
            ret = copy.deepcopy(other)
            for i in range(0,len(ret.ps)):
                ret.ps[i] = self * ret.ps[i]
        if type(other) in [float,int,str] or isinstance(other,coefficient.coefficient):
            ret.coeff = ret.coeff * other
        return ret
    
    
    def __sub__(self,other):
        self.sanityCheck()
        return self + (other * (-1))
    ##############################################################################################################        
    ########### safety checks for debugging
    ##############################################################################################################
    def sanityCheck(self):
        assert isinstance(self.symbs, list)
        for i in self.symbs:
            assert isinstance(i,str)
        ######################
        assert isinstance(self.rels, dict)
        
        for i in self.rels.keys():
            assert isinstance(i,tuple)
            for j in i:
                assert j in self.symbs
        
        for i in self.rels.values():
            assert isinstance(i,list)
            for j in i:
                assert j in self.symbs
        #######################
        assert isinstance(self.coeff,coefficient.coefficient)
        
        #######################
        assert isinstance(self.vs,list)
        for i in self.vs:
            assert i in self.symbs
