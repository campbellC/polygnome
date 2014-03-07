from coefficient import coefficient


class monomial:
    """A monomial is just a list of variables with a coefficient"""
    def __init__(self,coefficient = coefficient(),symbols=[]):
        self.coeffs = coefficient
        self.symbs = symbols
    
    