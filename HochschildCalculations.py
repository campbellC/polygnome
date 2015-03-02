from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
from pureTensor import pureTensor
from tensor import tensor
import copy
import re


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


def mono(vs,c=coefficient()):
    return monomial(vs,symbs,rels,c)
x1 = mono(["x1"])
x2 = mono(["x2"])
x3 = mono(["x3"])
x4 = mono(["x4"])
zero = mono([],coefficient({'':0}))



def generic(letter,n):
    answer = polynomial()
    nums = {0:["0"], 1:["1",'2','3','4'],2:['21','22','23','24','11','13','14','33','34','44']}[n]
    letterCoeffs = []
    for i in nums:
        letterCoeffs.append(letter+i)
    for (i,j) in zip(letterCoeffs,nums):
        localMono = mono([])
        if n ==0:
            answer = answer + mono([],coefficient({i:1}))
        if n ==1:
            answer = answer + {"1":x1,"2":x2,"3":x3,"4":x4}[j] * i
        elif n ==2:
            answer = answer + {'21':x2*x1,'22':x2*x2,'23':x2*x3,\
                               '24':x2*x4,'11':x1*x1,'13':x1*x3,\
                               '14':x1*x4,'33':x3*x3,'34':x3*x4,'44':x4*x4}[j]*i
    return answer 
            
    


def g(aRc, deg =1):#this acts on K1
    aRc.sort()
    aRc = copy.deepcopy(aRc)
    assert isinstance(aRc, pureTensor) or isinstance(aRc,tensor)
    if isinstance(aRc,tensor):
        flag = True
        for i in aRc.ps:
            if flag:
                answer = g(i,deg)
                flag = False
            else:
                answer = answer + g(i,deg)
            
    else:
        c = aRc.coeff
        assert aRc.degree() == 3
        if not aRc.monos[0].isNum():
            a = copy.deepcopy(aRc.monos[0])
            aRc.monos[0].vs = []
            answer =  a * g(aRc,deg)
        elif not aRc.monos[2].isNum():
            b = copy.deepcopy(aRc.monos[2])
            aRc.monos[2].vs = []
            answer =  g(aRc,deg) * b
        elif aRc.monos[1] == x1:
            answer =  generic('a',deg)*c
        elif aRc.monos[1] == x2:
            answer =  generic('b',deg)*c
        elif aRc.monos[1] == x3:
            answer =  generic('c',deg)*c
        elif aRc.monos[1] == x4:
            answer =  generic('d',deg)*c
    answer.sort()
    return answer





r1 = pureTensor([x3,x1,mono([])])+pureTensor([x1,x3,mono([])])*(-1)+pureTensor([mono([]),x3,x1])+pureTensor([mono([]),x1,x3])*(-1)
r2 = pureTensor([x4,x2,mono([])])+pureTensor([x2,x4,mono([])])*(-1)+pureTensor([mono([]),x4,x2])+pureTensor([mono([]),x2,x4])*(-1)
r3 = pureTensor([x4,x1,mono([])])+pureTensor([x2,x3,mono([])])*(-1)+pureTensor([mono([]),x4,x1])+pureTensor([mono([]),x2,x3])*(-1)
r4 = pureTensor([x1,x2,mono([])])+pureTensor([x2,x3,mono([])])*(-1)+pureTensor([mono([]),x1,x2])+pureTensor([mono([]),x2,x3])*(-1)
r5 = pureTensor([x3,x2,mono([])])+pureTensor([x1,x4,mono([])])*(-1)+pureTensor([mono([]),x3,x2])+pureTensor([mono([]),x1,x4])*(-1)
r6 = pureTensor([x4,x3,mono([])])+pureTensor([x1,x4,mono([])])*(-1)+pureTensor([mono([]),x4,x3])+pureTensor([mono([]),x1,x4])*(-1)
    


rs = [r1,r2,r3,r4,r5,r6]
for i in rs:
    i.sort()


#f3 = open('out3.txt','w')
#count = 0
#for l in rs:
#    count +=1
#    z = g(l,1)
#    z.sort()
#    for j in z.monos:
#        ks =[]
#        for k in j.coeff.coeffs:
#            if j.coeff.coeffs[k]==-1:
#                k = "-"+k
#            elif j.coeff.coeffs[k] ==0:
#                continue
#            ks.append(k)
#        eq = "+".join(k for k in ks)
#        eq += "=0"
#        if eq == "=0":
#            continue
#        
#        f3.write(eq)
#        f3.write("\n")
#f3.close()


def f(aRc,deg=1): #this acts on k2
    aRc.sort()
    aRc = copy.deepcopy(aRc)
    assert isinstance(aRc, pureTensor) or isinstance(aRc,tensor)
    if isinstance(aRc,tensor):
        flag = True
        for i in aRc.ps:
            if flag:
                answer = f(i,deg)
                flag = False
            else:
                answer = answer + f(i,deg)
          
    else:
        c = aRc.coeff
        assert aRc.degree() == 3
        if not aRc.monos[0].isNum():
            a = copy.deepcopy(aRc.monos[0])
            aRc.monos[0]=mono([])
            answer = a * f(aRc,deg)
        elif not aRc.monos[2].isNum():
            b = copy.deepcopy(aRc.monos[2])
            aRc.monos[2] = mono([])
            answer = f(aRc,deg) * b
        elif aRc.monos[1] == {("x3" ,"x1") : ["x1", "x3"]}:
            answer = generic('a',deg) * c
        elif aRc.monos[1] == {("x4", "x2") : ["x2", "x4"]}:
            answer = generic('b',deg)*c
        elif aRc.monos[1] == {("x4", "x1") : ["x2", "x3"]}:
            answer = generic('c',deg)*c
        elif aRc.monos[1] == {("x1", "x2") : ["x2", "x3"]}:
            answer = generic('d',deg)*c
        elif aRc.monos[1] == {("x3", "x2") : ["x1", "x4"]}:
            answer = generic('k',deg)*c
        elif aRc.monos[1] == {("x4", "x3") : ["x1", "x4"]}:
            answer = generic('f',deg)*c
    answer.sort()
    return answer  


temp = pureTensor([mono([]),{("x3",'x1') : ['x1','x3']},mono([])])
#print f(temp,2)
#print generic('a',0)
#print x1 * generic('a',1)

#print generic('a',2)
k3_1 = pureTensor([x3,r[4],mono([])]) + pureTensor([x1,r[6],mono([])]) + pureTensor([x1,r[5],mono([])])*(-1) +\
pureTensor([mono([]),r[1],x2])*(-1) + pureTensor([mono([]),r[5],x3])

k3_2 = pureTensor([x4,r[1],mono([])])+ pureTensor([x1,r[3],mono([])])*(-1) +\
pureTensor([mono([]),r[6],x1])*(-1)  + pureTensor([mono([]),r[4],x3])*(-1)+ pureTensor([mono([]),r[3],x3])

k3_3 = pureTensor([x4,r[5],mono([])])+ pureTensor([x1,r[2],mono([])])*(-1) +\
pureTensor([mono([]),r[6],x2])*(-1)  + pureTensor([mono([]),r[4],x4])*(-1)+ pureTensor([mono([]),r[3],x4])

k3_4 = pureTensor([x4,r[4],mono([])])+ pureTensor([x2,r[6],mono([])])+ pureTensor([x2,r[5],mono([])])*(-1) +\
pureTensor([mono([]),r[3],x2])*(-1)+ pureTensor([mono([]),r[2],x3])



k3_1.sort()
k3_2.sort()
k3_3.sort()
k3_4.sort()

k3basis = [k3_1,k3_2,k3_3,k3_4]


#
#f1 = open('out4.txt','w')
#count = 0
#for i in k3basis:
#    count += 1
#    z = f(i,2)
#    z.sort()
#    for j in z.monos:
#        ks =[]
#        for k in j.coeff.coeffs:
#            if j.coeff.coeffs[k]==-1:
#                k = "-"+k
#            elif j.coeff.coeffs[k] == 0:
#                continue
#            ks.append(k)
#        eq = "+".join(k for k in ks)
#        eq += "=0"
#        if eq == "=0":
#            continue
#        f1.write(eq)
#        print eq, j
#        f1.write('\n')
#            
#            
#f1.close()
#
#


#def imageCalcK1(abcd):
#    a = abcd[0]
#    b = abcd[1]
#    c = abcd[2]
#    d = abcd[3]
#    return [x3*a - x1*c + c*x1-a*x3,\
#            x4*b-x2*d+d*x2-b*x4,\
#            x4*a-x2*c+d*x1-b*x3,\
#            x1*b-x2*c+a*x2-b*x3,\
#            x3*b-x1*d+c*x2-a*x4,\
#            x4*c-x1*d+d*x3-a*x4]
#

#count = 0
#basis = []
#while True:
#    
#    temp = [zero for _ in range(4)]
#    temp[count / 4] ={0: x1, 1:x2,2:x3,3:x4}[count % 4]
#    basis.append(temp)
#    count +=1
#    if count == 16:
#        break



def imageCalcK2(abcdef):
    a=abcdef[0]
    b=abcdef[1]
    c = abcdef[2]
    d = abcdef[3]
    e=abcdef[4]
    f = abcdef[5]
    return [x3*d + x1*f-x1*e-a*x2+e*x3,\
            x4*a-x1*c-f*x1-d*x3+c*x3,\
            x4*e-x1*b-f*x2-d*x4+c*x4,\
            x4*d+x2*f-x2*e-c*x2+b*x3]

basis = []


count = 0
while True:
    temp = [zero for _ in range(6)]
    temp[count / 10] = {0: x2*x1, 1: x2*x2,2:x2*x3,3:x2*x4,\
                       4: x1*x1, 5: x1*x3, 6: x1*x4,\
                       7:x3*x3, 8: x3*x4,\
                       9: x4*x4}[count % 10]
    count +=1
    basis.append(temp)
    if count == 60:
        break

f1 = open('ImageK2.txt','w')
for i in basis:
    f1.write("\\( \n \\left( \n \\begin{array}{c}\n")
    for j in imageCalcK2(i):
        if j== "":
            f1.write( "0 \\\\")
        else:
            tempStr =  re.sub('x','x_',j.__repr__())
            f1.write(tempStr)
            f1.write(" \\\\ \n")
    f1.write("\\end{array} \n \\right) \\),\n")
