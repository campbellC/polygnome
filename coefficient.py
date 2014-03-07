class coefficient():
    """coefficient of monomial"""
    def __init__(self,coeffs = {}):
        self.coeffs = coeffs
        self.sanityCheck()
    
    
    def sanityCheck(self):
        assert isinstance(self.coeffs,dict)
        for i in self.coeffs.keys():
            assert isinstance(i,str)
        for i in self.coeffs.values():
            assert type(i) in [float,int]
