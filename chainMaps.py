import pureTensor
import relation
from tensor import tensor
from monomial import monomial


def bimoduleMap(func):
    def g(tens):
        tens = tens.clean()
        answer = tensor()
        for i in tens:
            left =i[0]
            right = i[-1]
            middle = i.subTensor(1,len(i)-1)
            answer = answer + left * func(middle) * right
        return answer
    return g


@bimoduleMap
def k_2(tens):
    assert isinstance(tens,pureTensor.pureTensor)
    answer= tensor()
    rel =tens.monomials[0]
    for i in rel.leadingMonomial:
        answer = answer + tensor((i.submonomial(0,1),i.submonomial(1,2),monomial(1)))
        answer = answer + tensor((monomial(1),i.submonomial(0,1),i.submonomial(1,2)))
    for i in rel.lowerOrderTerms:
        answer = answer - tensor((i.submonomial(0,1),i.submonomial(1,2),monomial(1)))
        answer = answer + tensor((monomial(1),i.submonomial(0,1),i.submonomial(1,2)))
    return answer

@bimoduleMap
def b_n(tens): #TODO: this is broken, fix it
    assert isinstance(tens, pureTensor.pureTensor)
    answer = pureTensor.pureTensor((tens[0],)).tensorProduct(tens.subTensor(1,len(tens))).tensorProduct(monomial(1))
    for i in xrange(len(tens)-1):
        mono = tens[i] * tens[i+1]
        left = pureTensor.pureTensor(monomial(1)).tensorProduct( tens.subTensor(0,i))
        right = tens.subTensor(i+2,len(tens)).tensorProduct(monomial(1))
        answer = answer +((-1) ** (i+1)) * left.tensorProduct(mono).tensorProduct(right)
    answer = answer + (((-1) ** len(tens)) * pureTensor.pureTensor((monomial(1),)).tensorProduct(tens.subTensor(0,len(tens)-1).tensorProduct(tens[-1]))).clean()
    return answer



