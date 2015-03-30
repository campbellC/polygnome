from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
from pureTensor import pureTensor
from tensor import tensor
import copy
import re
from chainMaps import barMap
import networkx as nx


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

##need a function that takes an element of the the algebra and returns the sum of all possible paths divided by the number of paths

def newM2facmap(x):
    assert isinstance(x,monomial)
    if x.sorted():
        return (pureTensor([zero,zero,zero],coefficient({'':0})),)
    else:
        answer = tuple()
        for i in range(0,x.degree()-1):
            if (x.vs[i],x.vs[i+1]) in rels:
                answer += tuple((pureTensor([mono(x.vs[:i]),{(x.vs[i],x.vs[i+1]):rels[(x.vs[i],x.vs[i+1])]},mono(x.vs[i+2:])])+z) for z in newM2facmap(mono(x.vs[:i]+rels[(x.vs[i],x.vs[i+1])]+x.vs[i+2:])))
        return answer       

def newM2(x):
    assert isinstance(x,monomial)
    answer = pureTensor([zero,zero,zero],coefficient({'':0}))
    if x.sorted():
        return answer
    fac = newM2facmap(x)
    for i in fac:
        answer += i
    assert isinstance(answer,pureTensor) or isinstance(answer, tensor)
    return answer*(float(1)/len(newM2facmap(x)))

def facMap(tens):
    assert isinstance(tens,pureTensor) or isinstance(tens,tensor)
    ten = copy.deepcopy(tens)
    ret = tensor()
    ten.sort()
    if isinstance(ten,tensor):
        for i in ten.ps:
             fm = facMap(i)
             ret = ret + fm
        return ret
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
            answer = newM2(ten.monos[1]*ten.monos[2])
            assert isinstance(answer,pureTensor) or isinstance(answer, tensor)
            return answer
        


for i in newM2facmap(x1*x2*x3*x2*x4):
    print i
print newM2(x1*x2*x3*x2*x4)


##testing m3 code
#ys1=[x2,x1,x3,x4]
#xs=[x2,x1,x3,x4]
#for inum,i in enumerate(ys1):
#    for jnum,j in enumerate(ys1):
#        if inum <= jnum:
#            xs.append(i*j)
#        else:
#            continue
#        #for knum,k in enumerate(ys1):
#        #    if inum <= jnum and jnum <= knum:
#        #        xs.append(i*j*k)
#        #    else:
#        #        continue
#        #    
#
#print xs
#f1 = open("OutputOfm3Test.txt",'w')      
#for inum,i in enumerate(xs):
#    for jnum,j in enumerate(xs):
#        for knum,k in enumerate(xs):
#            if (i*j).sorted() or (j*k).sorted():
#                continue
#            else:
#                f1.write("1|"+i.__repr__()+"|"+j.__repr__()+"|"+k.__repr__()+"|1 --> ")
#                myTens = pureTensor([one,i,j,k,one])
#            #print myTens,"------>",barMap(myTens)
#                myOut = facMap(barMap(myTens))
#                print myTens, "DEBUG", barMap(myTens), myOut
#                myOut.sort()
#                f1.write(myOut.__repr__()+"\n\n")    
#            
#
#
#f1.close()
#f2 = open("OutputOfm3Test.txt",'r')
#f3 = open("latexOutputm3Test.txt",'w')
#f3.write("\\begin{align*}\n")
#for line in f2:
#    if line == "":
#        continue
#    line = re.sub(r"\-\->",r"&\\mapsto",re.sub(r"x",r"x_",line))
#    line = re.sub(r"{\('x_3', 'x_1'\): \['x_1', 'x_3'\]}",r"r_1",line)
#    line = re.sub(r"{\('x_4', 'x_2'\): \['x_2', 'x_4'\]}",r"r_2",line)
#    line = re.sub(r"{\('x_4', 'x_1'\): \['x_2', 'x_3'\]}",r"r_3",line)
#    line = re.sub(r"{\('x_1', 'x_2'\): \['x_2', 'x_3'\]}",r"r_4",line)
#    line = re.sub(r"{\('x_3', 'x_2'\): \['x_1', 'x_4'\]}",r"r_5",line)
#    line = re.sub(r"{\('x_4', 'x_3'\): \['x_1', 'x_4'\]}",r"r_6",line)
#    f3.write(line+"\\\\")
#f3.write("\\end{align*}")
#f2.close()
#f3.close()
#
#
#
#
#
