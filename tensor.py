import pureTensor

class tensor():
    """a list of pure tensors """
    
    def __init__(self,ps = []):
        self.ps=ps
        self.sanityCheck()
    
    
    
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
        flag = True
        if self.sorted():
            return
        for i in self.ps:
            i.sort()
        while not self.sorted():
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
        self.sanityCheck()
        
    
    def __repr__(self):
        return "+".join(x.__repr__() for x in self.ps)
    def sanityCheck(self):
       assert isinstance(self.ps,list)
       for i in self.ps:
            assert isinstance(i,pureTensor.pureTensor)
    
