import coefficient
import copy

class pureTensor():
    """Stores a pure tensor of any objects you like, it is up to you to handle the coefficient"""
    
    def __init__(self, monos = [],coeff = [coefficient.coefficient()]): 
        self.monos = monos
        self.coeff = coeff #a list of coefficients
        self.sanityCheck()
       
        
        
        
        
        
        
    ################################################################################################################################################
    ######################################################################## SORTING METHODS########################################################################
    ################################################################################################################################################
    
    def sorted(self):
        self.sanityCheck()
        for i in self.monos:
            if hasattr(i,'coeff'):
                if i.coeff != coefficient.coefficient({"":1}):
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
            if hasattr(i,'coeff'):
                if i.coeff != coefficient.coefficient({"":1}):
                    self.coeff.append(i.coeff)
                    i.coeff=coefficient.coefficient({"":1})
            if hasattr(i,'sort'):
                i.sort()
        self.sanityCheck()
        
    def safeSort(self):
        ret = copy.deepcopy(self)
        ret.sort()
        return ret.monos
    
    ################################################################################################################################################
    ################################################ __methods ##########################################################################################
    ################################################################################################################################################
    
        
    
    def __repr__(self):
        return "".join(i.__repr__() for i in self.coeff if (i.coeffs != coefficient.coefficient().coeffs))\
                               + "|".join(x.__repr__() for x in self.monos)
            
    
    
    
    ################################################################################################################################################
    ################################################Debugging code################################################################################################
    ################################################################################################################################################
    
    def sanityCheck(self):
        assert isinstance(self.monos,list)
        assert isinstance(self.coeff,list)
        for i in self.coeff:
            assert isinstance(i,coefficient.coefficient)
    
    
