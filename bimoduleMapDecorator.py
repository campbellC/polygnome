import pureTensor
class bimoduleMapDecorator(object):
    """
    File: chainMaps.py
    Author: Chris Campbell
    Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: A decorator that extends a function defined on a tensor algebra bilinearly with respect to some algebra.
    You must pass it the domain and codomain tensor algebras in order for it to reduce input and output for you.
    """
    def __init__(self, domain, codomain):
        self.domain = domain
        self.codomain = codomain

    def __call__(self,func):
        def wrapped_func(tens):
            if tens == 0:
                return self.codomain.zero()
            tens = tens.clean()
            tens = self.domain.reduce(tens)
            firstItem = True
            for pure in tens:
                left =pure[0]
                right = pure[-1]
                middle = pureTensor.pureTensor(1).tensorProduct(pure.subTensor(1,len(pure)-1)).tensorProduct(1)
                if firstItem:
                    answer = pure.coefficient * left * func(middle) * right
                    firstItem = False
                else:
                    answer = answer + pure.coefficient * left * func(middle) * right
            return self.codomain.reduce(answer)
        return wrapped_func
