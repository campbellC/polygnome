from pureTensor import pureTensor
import relation
from tensor import tensor
from monomial import monomial
from tensorAlgebra import tensorAlgebra
from algebra import algebra
def bimoduleMap(func): # This is a decorator that extends maps defined on pure tensors bilinearly
    def g(tens):
        if tens == 0:
            return tensor()
        tens = tens.clean()
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
        return answer
    return g


@bimoduleMap
def k_2withoutAlgebra(tens):
    assert isinstance(tens,pureTensor)
    answer= tensor()
    rel =tens.monomials[1]
    for i in rel.leadingMonomial:
        answer = answer + tensor((i.submonomial(0,1),i.submonomial(1,2),monomial(1)))
        answer = answer + tensor((monomial(1),i.submonomial(0,1),i.submonomial(1,2)))
    for i in rel.lowerOrderTerms:
        answer = answer - tensor((i.submonomial(0,1),i.submonomial(1,2),monomial(1)))
        answer = answer - tensor((monomial(1),i.submonomial(0,1),i.submonomial(1,2)))
    return answer

def k_2(tens,alg):
    freeAlgebra = algebra()
    K2 = tensorAlgebra([alg,freeAlgebra,alg])
    tens = K2.reduce(tens)
    answer = k_2withoutAlgebra(tens)
    K1 = tensorAlgebra([alg]*3)
    return K1.reduce(answer)


#We split up b_n into the basic map defined for any algebra, and then give the
#option of using b_n with an algebra that will reduce the output
@bimoduleMap
def b_nWithoutAlgebra(tens):
    assert isinstance(tens, pureTensor)
    assert len(tens) >= 2
    tens = tens.clean()
    if len(tens) == 2:
        return tens[0] * tens[1]
    else:
        answer = tens.subTensor(1,len(tens) )
        answer = answer - pureTensor(1).tensorProduct(tens[1]*tens[2]).tensorProduct(tens.subTensor(3,len(tens)))
        answer = answer + tens.subTensor(0,2).tensorProduct(b_nWithoutAlgebra(tens.subTensor(2,len(tens))))
        return answer

def b_n(tens,alg):
    tensAlg = tensorAlgebra([alg] * len(tens))
    tens = tensAlg.reduce(tens)
    tens = b_nWithoutAlgebra(tens)
    tensAlg = tensorAlgebra([alg] * len(tens))
    return tensAlg.reduce(tens)


def m_2(abcd,alg):
    B2 = tensorAlgebra([alg]*4)
    freeAlgebra = algebra()
    K2 = tensorAlgebra([alg,freeAlgebra,alg])
    abcd = B2.reduce(abcd)
    answer = tensor()
    for PT in abcd:
        assert isinstance(PT, pureTensor)
        assert len(PT) == 4
        PT = PT.clean()
        w = PT[1] * PT[2]
        sequence = alg.makeReductionSequence(w)
        for reductionFunction, weight in sequence:
            answer += PT.coefficient * weight * PT[0] \
                * pureTensor([reductionFunction.leftMonomial,
                              reductionFunction.relation,
                              reductionFunction.rightMonomial]) * PT[3]
    return K2.reduce(answer)

def m_1(abc,alg):
    K1 = B1 = tensorAlgebra([alg]*3)
    abc = B1.reduce(abc)
    answer = tensor()

    def helper(b):
        b = b.clean()
        helperAnswer = tensor()
        if b.degree() != 0:
            for i in range(b.degree()):
                helperAnswer += b.coefficient * pureTensor([b[0:i],b[i],b[i+1:]])
        return helperAnswer

    for PT in abc:
        assert len(PT) == 3
        answer += PT.coefficient * PT[0] * helper(PT[1]) * PT[2]
    return K1.reduce(answer)
