from math import factorial
from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
from pureTensor import pureTensor
from tensor import tensor
import copy
import re
from chainMaps import barMap
from gerstenhaberBracket import GerstenhaberBracket, interpretVectorAsFunctionOnK2, m2
from prettyTyping import *
c = coefficient()

symbs = ["x1", "x2","x3","x4"]
rels = { ("x3" ,"x1") : ["x1", "x3"],\
    ("x4", "x2") : ["x2", "x4"],\
    ("x4", "x1") : ["x2", "x3"],\
    ("x1", "x2") : ["x2", "x3"],\
    ("x3", "x2") : ["x1", "x4"],\
    ("x4", "x3") : ["x1", "x4"]}
r = {1: {("x3" ,"x1") : ["x1", "x3"]},\
    2: {("x4", "x2") : ["x2", "x4"]},\
    3: {("x4", "x1") : ["x2", "x3"]},\
    4:{("x1", "x2") : ["x2", "x3"]},\
    5:{("x3", "x2") : ["x1", "x4"]},\
    6:{("x4", "x3") : ["x1", "x4"]} }



def mono(vs=[],c=coefficient()):
    return monomial(vs,symbs,rels,c)
x1 = mono(["x1"])
x2 = mono(["x2"])
x3 = mono(["x3"])
x4 = mono(["x4"])
zero = mono([],coefficient({'':0}))
one = mono()




###################################################################################################################################################
####### Code to convert a vector in the degree three piece of K^3 into a vector readable by sage for linear algebra calculations  
###################################################################################################################################################


#the first thing that is needed is to take a vector of degree three things and convert it into a vector of 0's and 1's. This will ignore coefficients, as long 
#as the coefficient is non-zero.

#we have a natural order on the degree three monomials 222,221,223,224,...
##############################################################################################################################################################################################
#####################################_# these functions convert a monomial to a number and vice versa, i.e. the component in the vector space that these monomials correspond to
##############################################################################################################################################################################################
MonoToNumberlst = [{},{},{},{}]
variables = [x2,x1,x3,x4]
n1 = 0
n2 = 0
n3 =0
n4 = 0
for i in range(4):
    x = variables[i]
    MonoToNumberlst[0]["".join(i for i in x.vs)] = n1
    n1 +=1
    for j in range(4):
        if j < i:
            continue
        x = variables[i] * variables[j]
        MonoToNumberlst[1]["".join(i for i in x.vs)] = n2
        n2 +=1
        for k in range(4):
            if k < j:
                continue
            x = variables[i] * variables[j] * variables[k]
            MonoToNumberlst[2]["".join(i for i in x.vs)] = n3
            n3 += 1
            for l in range(4):
                if l < k:
                    continue
                x= variables[i] * variables[j] * variables[k] * variables[l]
                MonoToNumberlst[3]["".join(i for i in x.vs)] = n4
                n4 +=1
def monoToNumber(M):
    return MonoToNumberlst[M.degree()-1]["".join(i for i in M.vs)]



NumberToMonolst = [{v : k for k, v in MonoToNumberlst[i].iteritems()} for i in range(4)]
for i in range(4):
    for v in NumberToMonolst[i]:
        lst = re.split(r"(x\d)",NumberToMonolst[i][v])
        lst = [x for x in lst if x != ""]
        NumberToMonolst[i][v] = mono(lst)

def numberToMono(num,degree):
    return NumberToMonolst[degree-1][num]
##############################################################################################################################################################################################
##################################### u# using these numberings above we can convert a vector of monomials into a vector of numbers and vice versa so that sage can work with them
##############################################################################################################################################################################################
def nCr(n,r):
    f = factorial
    return f(n) / f(r) / f(n-r)

def KnToVectSplitUp(vect,n,degree):#This function requires you to state the degree as this saves unnecessary work on behalf of the coder! it assumes of course that you are only looking at homogenous vectors
    monomialDimension = nCr(3 + degree, 3)
    totalDimension = nCr(4,n) * monomialDimension
    answer = [] 
    def monoToVect(m,component):
        mVect = [0] * totalDimension
        mCoeff = m.coeff 
        component = component * monomialDimension + monoToNumber(m)
        mVect[component] = 1
        return (mCoeff,mVect)
    for inum,i in enumerate(vect):
        i.sort()
        if isinstance(i,polynomial):
            for m in i.monos:
                if m.isZero():
                    continue
                answer.append(monoToVect(m,inum))
        else:
            if i.isZero():
                continue
            answer.append(monoToVect(i,inum))
    return answer
def vectOfNumsSplitUpToVect(vect,dimension): #TODO: modify this function to convert to symbolic vectors as well as number vectors
    answer = [0] * dimension
    for i in vect:
        assert i[0].isNum()
        component = None;
        for jnum,j in enumerate(i[1]):
            if j != 0:
                component = jnum
                break
        answer[component] += i[0].coeffs[""]
    return answer

def vectSplitUpToKn(vect,n,degree):
    monoDimension = nCr(3+degree,3)
    rankOfKn = nCr(4,n)
    vectOfMonos = [zero] * rankOfKn 
    totalDimension = monoDimension * rankOfKn
    for i in vect:
        assert isinstance(i[0],coefficient) and len(i[1]) == totalDimension
        mCoeff = i[0]
        position = 0
        if i[1] == [0 for _ in xrange(totalDimension)]:
                continue
        for inum in xrange(totalDimension):
            if i[1][inum] == 1:
                position = inum
                break
        component = position // monoDimension
        monoNum = position % monoDimension 
        vectOfMonos[component] = vectOfMonos[component] + numberToMono(monoNum,degree) * mCoeff
    return vectOfMonos
def vectToVectSplitUp(vect):
    dimension = len(vect)
    answer = []
    for inum,i in enumerate(vect):
        if i != 0:
            mCoeff = coefficient.fromNumber(i)
            mVect = [0] * dimension
            mVect[inum] = 1
            answer.append( (mCoeff,mVect))
    return answer

        
