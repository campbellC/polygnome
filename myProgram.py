from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
from pureTensor import pureTensor
from tensor import tensor
from chainMaps import barMap,k2,m1,facMap
import random
import time

from itertools import product
symbs = ["x1", "x2","x3","x4"]
rels = { ("x3" ,"x1") : ["x1", "x3"],\
    ("x4", "x2") : ["x2", "x4"],\
    ("x4", "x1") : ["x2", "x3"],\
    ("x1", "x2") : ["x2", "x3"],\
    ("x3", "x2") : ["x1", "x4"],\
    ("x4", "x3") : ["x1", "x4"]}

def mono(vs,c=coefficient()):
    return monomial(vs,symbs,rels,c)

x1 = mono(["x1"])
x2 = mono(["x2"])
x3 = mono(["x3"])
x4 = mono(["x4"])
##############################################
#############Fuzz testing#######################
##############################################
#def randMono(length):
#    vs = []
#    for i in range(0,length):
#        vs.append(random.choice(symbs))
#    return mono(vs)
#NO_EXPERIMENTS = 1000
#MAX_LENGTH = 5
#random.seed()
#
#
#open("FalseDetection",'w').write("BEGIN\n\n")
#for i in range(0,NO_EXPERIMENTS):
#    n = random.randrange(1,MAX_LENGTH)
#    m = random.randrange(1,MAX_LENGTH)
#    a = randMono(n)
#    b = randMono(m)
#    z = pureTensor([mono([]),a,b,mono([])])
#    z.sort()
#    if (not (k2(facMap(z)) - m1(barMap(z))).isZero()):
#        print "failure on",a
#        print b, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#        
#        open("FalseDetection",'a').write("failure on: a = ")
#        open("FalseDetection",'a').write(a)
#        open("FalseDetection",'a').write("\n")
#        open("FalseDetection",'a').write("b = ")
#        open("FalseDetection",'a').write(b)
#        open("FalseDetection",'a').write("\n--------------------\n")
#        
#        
#        
#        
#        
#    else:
#        print "True", a
#        print b

##############################################
#############Systematic testing#######################
##############################################
MIN_LENGTH = 4
MAX_LENGTH = 7
def monosOfDegree(n):
    assert n > 0
    if n == 1:
        return [x1,x2,x3,x4]
    else:
        ret = []
        for i in [x1,x2,x3,x4]:
            for j in range(0,len(monosOfDegree(n-1))):
                ret.append(monosOfDegree(n-1)[j]*i)
        for i in ret:
            i.sort()
        return remDups(ret)

def dupTest(x,y = None):#true if duplicate is detected
    if isinstance(x,monomial):
        return x.vs == y.vs
    if isinstance(x,list):
        for i in x:
            for j in x:
                if i is j:
                    continue
                else:
                    if dupTest(i,j):
                        return True
        return False
def remDups(xs):
    assert isinstance(xs,list)
    if not dupTest(xs):
        return xs
    else:
        for i in xs:
            for j in range(0,len(xs)):
                if i is xs[j]:
                    continue
                else:
                    if dupTest(i,xs[j]):
                        return remDups(xs[:j]+xs[j+1:])
                    
     
for n in range(MIN_LENGTH,MAX_LENGTH):
    for m in range(MIN_LENGTH,MAX_LENGTH):
        for a,b in product(monosOfDegree(n),monosOfDegree(m)):
            start_time = time.time()
            m = a*b
            print time.time()-start_time, "spend on multiplication"
            start_time = time.time()
            if m.sorted():
                print time.time() - start_time, " spent checking sorted"
                continue
            print time.time() - start_time, " spent checking sorted"
            z = pureTensor([mono([]),a,b,mono([])])
            z.sort()
            print time.time()-start_time, "spent sorting z"
            start_time = time.time()
            if (not (k2(facMap(z)) - m1(barMap(z))).isZero()):
                print "failure on",a
                print b, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    
                open("FalseDetection",'a').write("failure on: a = ")
                open("FalseDetection",'a').write(a)
                open("FalseDetection",'a').write("\n")
                open("FalseDetection",'a').write("b = ")
                open("FalseDetection",'a').write(b)
                open("FalseDetection",'a').write("\n--------------------\n")
                    
                    
                    
                    
                    
            else:
                print time.time()-start_time, "spent checking is zero"
                print "True", a
                print b


print x1.sorted()




##Data set for building m3 and beyond





