import coefficient
import copy
import  tensor
import monomial
import polynomial

class pureTensor():
    """Stores a pure tensor of any objects you like, it is up to you to handle the coefficient"""
    
    def __init__(self, monos = [],coeff = coefficient.coefficient()): 
        self.monos = copy.deepcopy(monos)
        self.coeff = copy.deepcopy(coeff) 
        self.sanityCheck()
       
    def isZero(self):
        self.sort()
        return self.coeff.isZero()
        
        
        
    def degree(self):
        return len(self.monos)
    
    ################################################################################################################################################
    ######################################################################## SORTING METHODS########################################################################
    ################################################################################################################################################
    
    def sorted(self):
        self.sanityCheck()
        for i in self.monos:
            if hasattr(i,'coeff'):
                if i.coeff.coeffs != {"":1}:
                    return False
            if hasattr(i,'sorted'):
                if not i.sorted():
                    return False
        return True
    
    def sort(self):
        self.sanityCheck()
        if self.sorted():
            return
        for i in self.monos:
            if hasattr(i,'sort'):
                i.sort()
            if hasattr(i,'coeff'):
                if i.coeff.coeffs != {"":1}:
                    self.coeff = self.coeff.times(i.coeff)
                    i.coeff=coefficient.coefficient({"":1})
            
        self.sanityCheck()
        
    def safeSort(self):
        ret = copy.deepcopy(self)
        ret.sort()
        return ret.monos
    
    def addable(self,other):
        ret = copy.deepcopy(self)
        s1 = ret.safeSort()
        s2 = other.safeSort()
        for i in range(0, len(s1)):
            if hasattr(s1[i],'vs') and hasattr(s2[i],'vs'):  #This will certainly need more cases adding
                if s1[i].vs != s2[i].vs:
                    return False
            else:
                if s1[i] != s2[i]:
                    return False
        
        return True
    
    ################################################################################################################################################
    ################################################ __methods__ ##########################################################################################
    ################################################################################################################################################
    
        
    
    def __repr__(self):
    	if self.coeff.__repr__() == "":
    	   return "|".join(x.__repr__() for x in self.monos)
    	elif self.coeff.__repr__() == "-":
    	   return self.coeff.__repr__()  + "|".join(x.__repr__() for x in self.monos)
    	else:
           return self.coeff.__repr__() +"*" + "|".join(x.__repr__() for x in self.monos)
            
    
    
    def __add__(self,other):
        self.sanityCheck()
        if isinstance(other,pureTensor):
            ret = copy.deepcopy(self)
            if self.addable(other):
                    ret.coeff = ret.coeff + other.coeff
                    return ret    
            else:
                ret = tensor.tensor([ret,copy.deepcopy(other)])
                ret.sort()
                return ret
        if isinstance(other,tensor.tensor):
            ret = copy.deepcopy(other)
            ret.ps.append(copy.deepcopy(self))
            ret.sort()
            return ret
    def __mul__(self,other):
        ret = copy.deepcopy(self)
        if isinstance(other,monomial.monomial):
            ret.monos[-1] = ret.monos[-1] * other
            ret.sort()
        if isinstance(other,polynomial.polynomial):
            print "you haven't coded this yet, puretensor * polynomial"
        if type(other) in [float,int] or isinstance(other,coefficient.coefficient):
            ret.coeff = ret.coeff * other
        
        return ret
       
    def __sub__(self,other):
        self.sanityCheck()
        return self + (other * (-1))
      
    ################################################################################################################################################
    ################################################Debugging code################################################################################################
    ################################################################################################################################################
    
    def sanityCheck(self):
        assert isinstance(self.monos,list)
        assert isinstance(self.coeff,coefficient.coefficient)
    
    
