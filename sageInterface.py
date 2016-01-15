import sage.all as sage
from algebrasOfInterest import A,x1,x2,x3,x4,Aq,bases
from vector import vector
from coefficient import coefficient


# Need a set of functions to take a vector v of polynomials of length n to a
# vector in sage. Since we are only interested in these two algebras, we do this
# by writing some functions which convert one to the other. We handle quotients
# by inspection (e.g. taking 1/q we multiply it by q first. Since we are doing
# linear algebra this is fine.

K = sage.FunctionField(sage.QQ,'q')
q = K.gen()
# All calculations happen in rationals with q, those for the A case just don't
# use q.

dimensionOfKnOverA=[1,4,6,4,1]


def dimensionOfKn(n,degree):
    return dimensionOfKnOverA[n] * len(bases[degree])

#This will convert e.g. [x1,0,0,0] into (0,1,0,0,0,...). i.e. it makes a Vector
# it maps (k^n)^m --> k^(nm) in the normal way
def gnomeVectorToSage(vec,n,degree):
    dimension = dimensionOfKn(n,degree)
    V = sage.VectorSpace(K,dimension)
    answer = V.zero()
    for index, poly in enumerate(vec):
        if poly.isZero():
            continue
        else:
            currentBaseIndex = index * len(bases[degree])
            for mono in poly:
                normalisedMono = mono.withCoefficientOf1()
                newIndex = currentBaseIndex + bases[degree].index(normalisedMono)
                answer = answer + V.basis()[newIndex] * gnomeCoeffToSage(mono.coefficient)
    return answer


def gnomeCoeffToSage(coeff):
    coeff = coeff.clean()
    #coeff is something like 1 + 2q + 3 qq + 4 qqq and so only
    answer = K.zero()
    for qs in coeff:
        numOfQs = len(qs)
        qPower = 1
        for x in range(numOfQs):
            qPower = qPower * q
        answer = answer + qPower * coeff[qs]
    return answer


def sageCoeffToGnome(coeff): #parse sage variables as strings and create gnome coefficients
    answer = coefficient(0)
    if coeff != 0:
        assert coeff.denominator() == 1
        coeff = repr(coeff) #get the string representation
        coeff = coeff.replace('-','+-')
        coeff = coeff.split('+')
        answer = coefficient(0)
        for term in coeff:
            if 'q' in term:
                coefficientOfq = 1
                powerOfq = 1
                if term[0] == '-':
                    coefficientOfq = -1
                for index,char in enumerate(term):
                    if char == '*':
                        coefficientOfq = int(term[:index])
                        continue
                    if char == '^':
                        powerOfq = int(term[index+1:])
                        break
                answer = answer + coefficient('q' * powerOfq) * coefficientOfq
            else:
                answer = answer + int(term)

    return answer

def sageVectToGnome(vec,degree): #this clear denominators for this vector
    for term in vec:
        if term.denominator() != 1:
            return sageVectToGnome(vec * term.denominator(),degree)
    answer = [coefficient(0)]
    for index,term in enumerate(vec):
        coeff = sageCoeffToGnome(term)
        currentBaseIndex = index // len(bases[degree])
        basisIndex = index - currentBaseIndex *len(bases[degree])
        if currentBaseIndex == len(answer):
            answer.append(coefficient(0))
        answer[-1] = answer[-1] + bases[degree][basisIndex] * coeff
    return vector(answer)

test = vector([x1*x2,x2*x2,x3*x1+x4*x4*'qq',x4*x4*'q']).reduceWithRespectTo(A)
assert sageVectToGnome(gnomeVectorToSage(test,n=1,degree=2),2) == test








