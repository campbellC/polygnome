class polynomial:
    """A polynomial with it's own defined relations"""
    
    

    def __init__(self,symbs=[],relations={},monomials=[]):
        self.symbs = symbs
        self.relations = relations
        self.monomials = monomials
        self.sanityCheck()
    
    
    def sanityCheck(self):
        assert isinstance(self.symbs, list)
        for i in self.symbs:
            assert isinstance(i,str)
        ####################################################
        assert isinstance(self.relations, dict)
        
        for i in self.relations.keys():
            assert isinstance(i,list)
            for j in i:
                assert j in self.symbs
        
        for i in self.relations.values():
            assert isinstance(i,list)
            for j in i:
                assert j in self.symbs
        #######################
        assert isinstance(self.monomials,list)
        
    def __repr__(self):
        self.sanityCheck()
        return "".join(x for x in self.symbs)




def main():
    x = polynomial(["a1","a2"])
    print x
    
if __name__ == '__main__':
    main()