from pureTensor import pureTensor
import relation
from tensor import tensor
from monomial import monomial
from tensorAlgebra import tensorAlgebra
from algebra import algebra


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
                return tensor()
            tens = tens.clean()
            tens = self.domain.reduce(tens)
            firstItem = True
            for pure in tens:
                left =pure[0]
                right = pure[-1]
                middle = pureTensor(1).tensorProduct(pure.subTensor(1,len(pure)-1)).tensorProduct(1)
                if firstItem:
                    answer = pure.coefficient * left * func(middle) * right
                    firstItem = False
                else:
                    answer = answer + pure.coefficient * left * func(middle) * right
            return self.codomain.reduce(answer)
        return wrapped_func

def b_n(tens,alg):
    domain = tensorAlgebra([alg] * len(tens))
    codomain = tensorAlgebra([alg] * (len(tens) - 1))

    @bimoduleMapDecorator(domain,codomain)
    def b_nInner(tens):
        assert isinstance(tens, pureTensor)
        assert len(tens) >= 2
        tens = tens.clean()
        if len(tens) == 2:
            return tens[0] * tens[1]
        else:
            answer = tens.subTensor(1,len(tens) )
            answer = answer - pureTensor(1).tensorProduct(tens[1]*tens[2]).tensorProduct(tens.subTensor(3,len(tens)))
            answer = answer + tens.subTensor(0,2).tensorProduct(b_n(tens.subTensor(2,len(tens)), alg))
            return answer
    return b_nInner(tens)



def k_2(tens,alg):
    freeAlgebra = algebra()
    K1 = K2 = tensorAlgebra([alg,freeAlgebra,alg])

    @bimoduleMapDecorator(K2,K1)
    def k_2Inner(tens):
        assert isinstance(tens,pureTensor)
        answer= tensor()
        rel =tens.monomials[1]
        for i in rel.leadingMonomial:
            answer = answer + i.coefficient * pureTensor((i.submonomial(0,1),i.submonomial(1,2),monomial(1)))
            answer = answer + i.coefficient * pureTensor((monomial(1),i.submonomial(0,1),i.submonomial(1,2)))
        for i in rel.lowerOrderTerms:
            answer = answer - i.coefficient * pureTensor((i.submonomial(0,1),i.submonomial(1,2),monomial(1)))
            answer = answer - i.coefficient * pureTensor((monomial(1),i.submonomial(0,1),i.submonomial(1,2)))
        return answer
    return k_2Inner(tens)


def m_2(abcd,alg):
    B2 = tensorAlgebra([alg]*4)
    freeAlgebra = algebra()
    K2 = tensorAlgebra([alg,freeAlgebra,alg])

    @bimoduleMapDecorator(B2,K2)
    def m_2Inner(PT):
        assert isinstance(PT, pureTensor)
        assert len(PT) == 4
        PT = PT.clean()
        w = PT[1] * PT[2]
        answer = tensor()
        sequence = alg.makeReductionSequence(w)
        for reductionFunction, weight in sequence:
            answer += PT.coefficient * weight * PT[0] \
                * pureTensor([reductionFunction.leftMonomial,
                              reductionFunction.relation,
                              reductionFunction.rightMonomial]) * PT[3]
        return answer

    return m_2Inner(abcd)


def m_1(abc,alg):
    K1 = B1 = tensorAlgebra([alg]*3)

    @bimoduleMapDecorator(B1,K1)
    def m_1Inner(b):
        b = b[1].clean()
        answer = tensor()
        if b.degree() != 0:
            for i in range(b.degree()):
                answer += b.coefficient * pureTensor([b[0:i],b[i],b[i+1:]])
        return answer

    return m_1Inner(abc)







