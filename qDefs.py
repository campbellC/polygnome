from monomial import *
from coefficient import *
c = coefficient()
q = coefficient({'q':1})

symbs = ["x1", "x2","x3","x4"]
rels = { ("x3" ,"x1") : ["x1", "x3",c],\
    ("x4", "x2") : ["x2", "x4",q],\
    ("x4", "x1") : ["x2", "x3",c],\
    ("x1", "x2") : ["x2", "x3",c],\
    ("x3", "x2") : ["x1", "x4",q],\
    ("x4", "x3") : ["x1", "x4",c]}
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

variables = [x2,x1,x3,x4]
letterCoeffs = []
for i in 'abcdefghijklmnop':
    letterCoeffs.append(coefficient({i:1}))
genericVectFirstPosition = [zero,zero,zero,zero]
j = -1
for inum,i in enumerate(letterCoeffs):  #this for loop builds a generic function from k1 to A. first pos is where x1 goes etc
    if inum % 4 == 0:
        j = j + 1
    genericVectFirstPosition[j] = genericVectFirstPosition[j] + variables[inum % 4] * i

# Now to write the map from such a function to K2. That is, it takes a vector of size four and returns a vector
# of size six, each one being what it does to that relation
def vectToLatex(vect):
    print '\\left( \\begin{array}{c}'
    for i in vect:
        print i, '\\\\'
    print '\\end{array} \\right)'

def k1(vect):
    assert len(vect) == 4
    answer = [zero,zero,zero,zero,zero,zero]
    answer[0] = answer[0] + x3*vect[0] - x1*vect[2] +  vect[2] * x1 - vect[0] * x3
    answer[1] = answer[1] + x4*vect[1] - x2*vect[3]*q +vect[3] * x2 - vect[1] * x4*q
    answer[2] = answer[2] + x4*vect[0] - x2*vect[2] +  vect[3] * x1 - vect[1] * x3
    answer[3] = answer[3] + x1*vect[1] - x2*vect[2] +  vect[0] * x2 - vect[1] * x3
    answer[4] = answer[4] + x3*vect[1] - x1*vect[3]*q+ vect[2] * x2 - vect[0] * x4*q
    answer[5] = answer[5] + x4*vect[2] - x1*vect[3] +  vect[3] * x3 - vect[0] * x4
    return answer
def k2(vect):
    answer = [zero,zero,zero,zero]
    answer[0] = x3 * vect[3] - x1 * vect[4] + x1 * q * vect[5]
    answer[1] = x4 * vect[0] - x1 * vect[2]
    answer[2] = x4 * vect[4] - x1 * vect[1]
    answer[3] = x4 * vect[3] - x2 * vect[4] + x2 * q * vect[5]
    return answer


# print 'From here are the images of k1\n \('
# j = -1
# n = 0
# for i in range(16):
#     genericVectFirstPosition = [zero,zero,zero,zero]
#     if i % 4 == 0:
#         j = j + 1
#     genericVectFirstPosition[j] = genericVectFirstPosition[j] + variables[i % 4]
#     vectToLatex(k1(genericVectFirstPosition))
#     n = n+ 1 
#     if n % 4 == 0:
#          print '\\) \n\n \\('
# 
# print '\)'
print 'From here are the images of k2\n \('
n = 0
for i in range(6):
    for j in range(4):
        for k in range(j,4):
            n = n + 1
            genericVectFirstPosition = [zero,zero,zero,zero,zero,zero]
            genericVectFirstPosition[i] = genericVectFirstPosition[i] + variables[j] * variables[k]
            vectToLatex(k2(genericVectFirstPosition))
            if n % 5 == 0:
                 print '\\)\n \n \\('
print '\)'
