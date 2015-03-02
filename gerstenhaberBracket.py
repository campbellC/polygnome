from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
from pureTensor import pureTensor
from tensor import tensor
import copy
import re
from chainMaps import barMap


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



basisK3temp = [pureTensor([x3,x1,x2])-pureTensor([x3,x2,x3])+pureTensor([x1,x4,x3])-pureTensor([x1,x1,x4])-pureTensor([x1,x3,x2])+pureTensor([x1,x1,x4]),\
           pureTensor([x4,x3,x1])-pureTensor([x4,x1,x3])-pureTensor([x1,x4,x1])+pureTensor([x1,x2,x3]),\
           pureTensor([x4,x3,x2])-pureTensor([x4,x1,x4])-pureTensor([x1,x4,x2])+pureTensor([x1,x2,x4]),\
           pureTensor([x4,x1,x2]) - pureTensor([x4,x2,x3])+pureTensor([x2,x4,x3])-pureTensor([x2,x1,x4])-pureTensor([x2,x3,x2])+pureTensor([x2,x1,x4])]

basisK3 = []
for tens in basisK3temp:
    tens = copy.deepcopy(tens)
    tens.sort()
    tempTens = tensor()
    for ptens in tens.ps:
        tempTens = tempTens + pureTensor([mono([]),ptens.monos[0],ptens.monos[1],ptens.monos[2],mono([])],ptens.coeff)
    basisK3.append(tempTens)

    ############code for m2########
        
def facMap(tens):
    assert isinstance(tens,pureTensor) or isinstance(tens,tensor)
    ten = copy.deepcopy(tens)
    ret = tensor()
    if isinstance(ten,tensor):
        for i in ten.ps:
             fm = facMap(i)
             ret = ret + fm 
    if isinstance(ten,pureTensor):
        ret = tensor([])
        assert ten.degree() == 4
        
        
        if not ten.monos[0].isNum():
            a = copy.deepcopy(ten.monos[0])
            ten.monos[0].vs = []
            return a * facMap(ten)
        elif not ten.monos[3].isNum():
            b = copy.deepcopy(ten.monos[3])
            ten.monos[3].vs = []
            return facMap(ten) * b
        else:
            x = ten.monos[1] * ten.monos[2]
            
            flag = True
            for i in x.facSeq():
                m = i[0]
                j = i[1]
                r = i[2]
                a = copy.deepcopy(m)
                a.vs = a.vs[:j]
                b = copy.deepcopy(m)
                b.vs = b.vs[j+2:]
                if flag:
                    ret = tensor([pureTensor([a,r,b])])
                    flag = False
                else:
                    ret = ret + pureTensor([a,r,b])
                
                
                
        coeff = ten.coeff
        
        ret = ret * coeff
        
    ret.sort()
    
    return ret
            
 



def m2(f):
    def m2f(abcd):
        return f(facMap(abcd))
    return m2f





def interpretVectorAsFunctionOnK2(v):
    def funV(aRc):
        aRc= copy.deepcopy(aRc)
        aRc.sort()
        assert isinstance(aRc,pureTensor) or isinstance(aRc,tensor)
        if isinstance(aRc,tensor):
            answer = zero
            for i in aRc.ps:
                answer = answer + funV(i)
        else:
            if not aRc.monos[0].isNum():
                a =  copy.deepcopy(aRc.monos[0])
                aRc.monos[0] = mono([])
                answer = a * funV(aRc)
            elif not aRc.monos[2].isNum():
                c = copy.deepcopy(aRc.monos[2])
                aRc.monos[2] = mono([])
                answer = funV(aRc) * c
            else:
                if aRc.monos[1] == {("x3" ,"x1") : ["x1", "x3"]}:
                    answer = v[0]*aRc.coeff
                elif aRc.monos[1] == {("x4", "x2") : ["x2", "x4"]}:
                    answer = v[1] *aRc.coeff
                elif aRc.monos[1] == {("x4", "x1") : ["x2", "x3"]}:
                    answer = v[2] *aRc.coeff
                elif aRc.monos[1] ==  {("x1", "x2") : ["x2", "x3"]}:
                    answer = v[3] *aRc.coeff
                elif aRc.monos[1] == {("x3", "x2") : ["x1", "x4"]}:
                    answer = v[4] *aRc.coeff
                elif aRc.monos[1] == {("x4", "x3") : ["x1", "x4"]}:
                    answer = v[5] *aRc.coeff
                else:
                    print "debugfunV undetected case"
        answer.sort()
        return answer
    return funV
        

  
        
    
def o0(f,g,abcde): #fo0g(a|b|c|d|e) = af(g(b|c)|d)e
    abcde = copy.deepcopy(abcde)
    abcde.sort()
    assert isinstance(abcde,pureTensor) or isinstance(abcde,tensor)
    if isinstance(abcde,tensor):
        
        answer = zero
        for i in abcde.ps:
            answer = answer + o0(f,g,i)
    else:
        if not abcde.monos[0].isNum():
            a = copy.deepcopy(abcde.monos[0])
            abcde.monos[0]= mono([])
            answer = a * o0(f,g,abcde)
        elif not abcde.monos[4].isNum():
            e = copy.deepcopy(abcde.monos[4])
            abcde.monos[4] = mono([])
            answer = o0(f,g,abcde) * e
        else:
            f
            b = abcde.monos[1]
            c = abcde.monos[2]
            d = abcde.monos[3]
            bc = pureTensor([mono([]),b,c,mono([])],coefficient())
            tempPoly = g(bc)
            if isinstance(tempPoly,polynomial):
                newbc = tensor()
                for i in tempPoly.monos:
                    newbc = newbc + pureTensor([mono([]),i,d,mono([])],abcde.coeff)
                        
            else:
                newbc = pureTensor([mono([]),tempPoly,d,mono([])],abcde.coeff)
            
            answer = f(newbc)
    
    answer.sort()
    return answer

def o1(f,g,abcde): #fo1g(a|b|c|d|e) = af(b|g(c|d))e
    abcde = copy.deepcopy(abcde)
    abcde.sort()
    assert isinstance(abcde,pureTensor) or isinstance(abcde,tensor)
    if isinstance(abcde,tensor):
        answer = zero
        for i in abcde.ps:
            answer = answer + o1(f,g,i)
    else:
        if not abcde.monos[0].isNum():
            a = copy.deepcopy(abcde.monos[0])
            abcde.monos[0]= mono([])
            answer =  a * o1(f,g,abcde)
        elif not abcde.monos[4] .isNum():
            e = copy.deepcopy(abcde.monos[4])
            abcde.monos[4] = mono([])
            answer =  o1(f,g,abcde) * e
        else:
            b = abcde.monos[1]
            c = abcde.monos[2]
            d = abcde.monos[3]
            cd = pureTensor([mono([]),c,d,mono([])],coefficient())
            tempPoly = g(cd)
            if isinstance(tempPoly,polynomial):
                newcd = tensor()
                for i in tempPoly.monos:
                    newcd = newcd + pureTensor([mono([]),b,i,mono([])],abcde.coeff)
                    
            else:
                newcd = pureTensor([mono([]),b,tempPoly,mono([])],abcde.coeff)
            answer = f(newcd)
    answer.sort()
    return answer

def o(f,g):
    def localO(abcde):
        return o0(f,g,abcde)-o1(f,g,abcde)
    return localO

def GerstenhaberBracket(f,g):
    def localBracket(abcde):
        return o(f,g)(abcde)+o(g,f)(abcde)
    return localBracket
