from pureTensor import pureTensor
import relation
from tensor import tensor
from monomial import monomial
from tensorAlgebra import tensorAlgebra
from algebra import algebra
from functionOnKn import functionOnKn

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
                middle = pureTensor(1).tensorProduct(pure.subTensor(1,len(pure)-1)).tensorProduct(1)
                if firstItem:
                    answer = pure.coefficient * left * func(middle) * right
                    firstItem = False
                else:
                    answer = answer + pure.coefficient * left * func(middle) * right
            return self.codomain.reduce(answer)
        return wrapped_func
##############################################################################
######  Chain map definitions
##############################################################################
def b_n(tens,alg):
    tens = tens.clean()
    if tens == 0:
        return 0
    else:
        for pure in tens:
            domain = tensorAlgebra([alg] * len(pure))
            codomain = tensorAlgebra([alg] * (len(pure) - 1))
            break

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
            if len(tens) != 3:
                answer = answer + tens.subTensor(0,2).tensorProduct(b_n(tens.subTensor(2,len(tens)), alg))
            return answer
    return b_nInner(tens)

def k_1(tens,alg):
    freeAlgebra = algebra()
    K1 = tensorAlgebra([alg,freeAlgebra,alg])
    K0 = tensorAlgebra([alg,alg])

    @bimoduleMapDecorator(K1,K0)
    def k_1Inner(pT):
        assert isinstance(pT,pureTensor)
        generator = pT[1]
        return pureTensor([generator,1])-pureTensor([1,generator])
    return k_1Inner(tens)

def k_2(tens,alg):
    freeAlgebra = algebra()
    K1 = K2 = tensorAlgebra([alg,freeAlgebra,alg])

    @bimoduleMapDecorator(K2,K1)
    def k_2Inner(tens):
        assert isinstance(tens,pureTensor)
        answer= tensor()
        rel =tens.monomials[1]
        for i in rel.leadingMonomial:
            answer = answer + i.coefficient * pureTensor((i.submonomial(0,1),i.submonomial(1,2), 1))
            answer = answer + i.coefficient * pureTensor((1,i.submonomial(0,1),i.submonomial(1,2)))
        for i in rel.lowerOrderTerms:
            answer = answer - i.coefficient * pureTensor((i.submonomial(0,1),i.submonomial(1,2), 1))
            answer = answer - i.coefficient * pureTensor((1,i.submonomial(0,1),i.submonomial(1,2)))
        return answer
    return k_2Inner(tens)

def k_3(tens,alg):
    freeAlgebra = algebra()
    K3 = K2 = tensorAlgebra([alg,freeAlgebra,alg])

    @bimoduleMapDecorator(K3,K2)
    def k_3Inner(pT):
        answer= tensor()
        doublyDefined = pT[1]
        for generator, rel in doublyDefined.leftHandRepresentation:
            answer = answer + pureTensor((generator,rel,1)).clean()
        for rel, generator in doublyDefined.rightHandRepresentation:
            answer = answer - pureTensor((1,rel,generator)).clean()
        return answer
    return k_3Inner(tens)

def i_1(tens,alg):
    freeAlgebra = algebra()
    B1 = tensorAlgebra([alg] * 3)
    K1 = tensorAlgebra([alg,freeAlgebra,alg])

    @bimoduleMapDecorator(K1,B1)
    def i_1Inner(pT):
        return pT
    return i_1Inner(tens)

def i_2(tens,alg):
    freeAlgebra = algebra()
    B2 = tensorAlgebra([alg] * 4)
    K2 = tensorAlgebra([alg,freeAlgebra,alg])

    @bimoduleMapDecorator(K2,B2)
    def i_2Inner(pT):
        answer = tensor()
        rel = pT[1]
        for term in rel.leadingMonomial:
            answer = answer + term.coefficient * pureTensor((1,term[0],term[1],1))
        for term in rel.lowerOrderTerms:
            answer = answer - term.coefficient * pureTensor((1,term[0],term[1],1))
        return answer
    return i_2Inner(tens)

def i_3(tens,alg):
    freeAlgebra = algebra()
    B3 = tensorAlgebra([alg] * 5)
    K3 = tensorAlgebra([alg,freeAlgebra,alg])

    @bimoduleMapDecorator(K3,B3)
    def i_3Inner(pT):
        answer = tensor()
        doublyDefined = pT[1]
        for generator, rel in doublyDefined.leftHandRepresentation:
            rightHandSide = generator * i_2(pureTensor([1,rel,1]),alg)
            answer = answer + pureTensor(1).tensorProduct(rightHandSide)
        return answer
    return i_3Inner(tens)


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


##############################################################################
######  Dualised chain maps
##############################################################################


def dualMap(chainMap):
    def functionFactory(func):
        def newfunc(tensor):
            return func(chainMap(tensor,func.algebra))
        return newfunc
    return functionFactory

m_1Dual = dualMap(m_1)
m_2Dual = dualMap(m_2)

k_2Dual = dualMap(k_2)
k_3Dual = dualMap(k_3)

def i_3Dual(func,alg,basisOfK3):
    images= []
    for i in basisOfK3:
        images.append(func(i_3(i,alg)))
    return functionOnKn(alg,basisOfK3,images)



##############################################################################
######  Gerstenhaber Bracket
##############################################################################

def o0(f,g,alg):
    B3 = tensorAlgebra([alg] * 5)

    @bimoduleMapDecorator(B3,alg)
    def localO(abcde):
        intermediate = g(pureTensor([1,abcde[1],abcde[2],1]))
        return f(pureTensor(abcde[0]).tensorProduct(intermediate).tensorProduct(abcde[3:]))
    return localO

def o1(f,g,alg):
    B3 = tensorAlgebra([alg] * 5)

    @bimoduleMapDecorator(B3,alg)
    def localO(abcde):
        intermediate = g(pureTensor([1,abcde[2],abcde[3],1]))
        return f(abcde[:2].tensorProduct(intermediate).tensorProduct(abcde[4]))
    return localO


def o(f,g,alg):
    def localO(abcde):
        return o0(f,g,alg)(abcde)-o1(f,g,alg)(abcde)
    return localO

def GerstenhaberBracket(f,g,basisOfK3):
    alg = f.algebra
    f = m_2Dual(f)
    g = m_2Dual(g)

    def localBracket(abcde):
        return o(f,g,alg)(abcde)+o(g,f,alg)(abcde)

    return i_3Dual(localBracket,alg,basisOfK3)
