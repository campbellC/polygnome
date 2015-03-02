from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
from pureTensor import pureTensor
from tensor import tensor
import copy
import re
from chainMaps import barMap
from gerstenhaberBracket import GerstenhaberBracket, interpretVectorAsFunctionOnK2, m2

c = coefficient()

symbs = ["x1", "x2","x3","x4"]
rels = { ("x3" ,"x1") : ["x1", "x3",c],\
    ("x4", "x2") : ["x2", "x4",c],\
    ("x4", "x1") : ["x2", "x3",c],\
    ("x1", "x2") : ["x2", "x3",c],\
    ("x3", "x2") : ["x1", "x4",c],\
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







###################################################################################################################################################
##########################################ACTION CODE ###############################################################
##############################################################################################################################




#####################Debugging code ###
#test = [x1*x3,zero,zero,x2*x3,x1*x4,zero]
#
#
#
#fun = interpretVectorAsFunctionOnK2(test)
#m2fun = m2(fun)
#tempvec = []
#for doublyDefined in basisK3:
#    doublyDefined = copy.deepcopy(doublyDefined)
#    tempvec.append( o0(m2fun,m2fun,doublyDefined)-o1(m2fun,m2fun,doublyDefined))
#print tempvec
#
##
#################################################


basisHH2temp = [[x1*x3,zero,zero,x2*x3,x1*x4,zero],\
            [x3*x3,zero,x1*x4,zero,zero,x3*x4],\
            [x1*x1,zero,zero,x2*x1,x2*x3,zero],\
            [zero,x4*x4,zero,zero, x3*x4,zero],\
            [zero,x2*x4,zero,zero,x1*x4,zero],\
            [zero, x2*x2, zero,zero,x2*x3,zero],\
            [zero,zero,zero,x1*x1,zero,x1*x3*(-1)],\
            [zero,zero,zero,x2*x2*(-1),zero,x2*x4]]
basisHH2 = []
for fun in basisHH2temp:
    fun = copy.deepcopy(fun)
    basisHH2.append(interpretVectorAsFunctionOnK2(fun))

   
#for i,f in enumerate(basisHH2):
#    for j,g in enumerate(basisHH2):
#        if j < i:
#            continue
#    
#        tempvec = []
#        m2f = m2(f)
#        m2g = m2(g)
#        gBracket = GerstenhaberBracket(m2f,m2g)       
#        for doublyDefined in basisK3:
#            doublyDefined = copy.deepcopy(doublyDefined)
#            tempvec.append(gBracket(doublyDefined))
#         
#        
#        print i,j
#        print "\n\n"
#        for m in tempvec:
#            print m
#        print "\n"
#


#geometricInfinitesimals = [mono(["x3","x3"],coefficient({"f":1}))-mono(["x1","x1"],coefficient({"e":1}))
#                            -mono(["x1","x3"],coefficient({"d":1}))*2, 
#                            mono(["x4","x4"],coefficient({"f":1}))-mono(["x2","x2"],coefficient({"e":1}))
#                            -mono(["x2","x4"],coefficient({"d":1}))*2,
#                             mono(["x1","x4"],coefficient({"f":1}))-mono(["x2","x1"],coefficient({"e":1}))
#                            -mono(["x2","x3"],coefficient({"d":1}))*2,
#                            mono(["x1","x4"],coefficient({"f":1}))-mono(["x2","x1"],coefficient({"e":1}))
#                            -mono(["x2","x3"],coefficient({"d":1}))*2 
#                            +mono(["x1","x1"],coefficient({"b":1}))
#                            #mono(["x2","x3"],coefficient({"a":1}))*2
#                            -mono(["x2","x4"],coefficient({"c":1})),
#                            mono(["x3","x4"],coefficient({"f":1}))-mono(["x2","x3"],coefficient({"e":1}))
#                            -mono(["x1","x4"],coefficient({"d":1}))*2,
#                            mono(["x1","x3"],coefficient({"b":1}))*(-1)
#                            #mono(["x1","x4"],coefficient({"a":1}))*(-2)
#                            +mono(["x4","x4"],coefficient({"c":1}))]
#
#for i in geometricInfinitesimals:
#    print i
#  
#
#tempvec = []
#m2f = m2(interpretVectorAsFunctionOnK2(geometricInfinitesimals))
#g = GerstenhaberBracket(m2f,m2f)
#print "g-bracket done"
#for doublyDefined in basisK3:
#
#    doublyDefined= copy.deepcopy(doublyDefined)
#    
#    tempvec.append(g(doublyDefined))
#    print "one calculation done", doublyDefined
#for i in tempvec:
#    for m in i.monos:
#        m.coeff.sort()
#    i.sort()
#    print i
#    
    #################TEMP CODE STARTS #######################
    geometricInfinitesimals = [mono(["x1","x1"],coefficient({"e":1}))*(-1),
                            mono(["x2","x2"],coefficient({"e":1}))*(-1),
                            zero,
                            mono(["x2","x1"],coefficient({"e":1}))*(-1)
                            +mono(["x1","x1"],coefficient({"b":1})),
                            mono(["x2","x3"],coefficient({"e":1}))*(-2),
                            mono(["x1","x3"],coefficient({"b":1}))*(-1)]

for i in geometricInfinitesimals:
    print i
  

tempvec = []
m2f = m2(interpretVectorAsFunctionOnK2(geometricInfinitesimals))
g = GerstenhaberBracket(m2f,m2f)
print "g-bracket done"
for doublyDefined in basisK3:

    doublyDefined= copy.deepcopy(doublyDefined)
    
    tempvec.append(g(doublyDefined))
    print "one calculation done", doublyDefined
for i in tempvec:
    for m in i.monos:
        m.coeff.sort()
    i.sort()
    print i
tempvec = []
g = GerstenhaberBracket(m2(basisHH2[2]),m2(basisHH2[6]))     
for doublyDefined in basisK3:

    doublyDefined= copy.deepcopy(doublyDefined)
    
    tempvec.append(g(doublyDefined))
    print "one calculation done", doublyDefined
print tempvec

#f1 = open('obstructionToGeometricDeformations.txt','w')
#
#
#for i in tempvec:
#
#    for j in i.monos:
#       newDict = {}
#       for chars in j.coeff.coeffs:
#          
#          if len(chars) == 2:
#             if chars[1] < chars[0]:
#                 tempstring = chars[1]+chars[0]
#                 
#                 if tempstring in newDict:
#                    newDict[tempstring]+=j.coeff.coeffs[chars]
#                 else:
#                    newDict[tempstring]=j.coeff.coeffs[chars]                
#             else:
#                if chars in newDict:
#                   newDict[chars]+=j.coeff.coeffs[chars]
#                else:
#                   newDict[chars]=j.coeff.coeffs[chars]
#       j.coeff = coefficient(newDict) 
#    f1.write(i.__repr__())
#    f1.write("\n\n")
#    print i
#    print "\n\n"
#    
#f1.close()
#
#
#






#
#
#
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
#            
#
#print xs
#f1 = open("OutputOfm3Test.txt",'w')      
#for inum,i in enumerate(xs):
#    #print inum, "Outer Loop debug"
#    for jnum,j in enumerate(xs):
#        for knum,k in enumerate(xs):
#            if (i*j).sorted() or (j*k).sorted():
#                #print i,j,k,"if clause debug"
#                continue
#            else:
#                #print i,j,k, "else clause debug"
#                f1.write("1|"+i.__repr__()+"|"+j.__repr__()+"|"+k.__repr__()+"|1 --> ")
#                myTens = pureTensor([one,i,j,k,one])
#            #print myTens,"------>",barMap(myTens)
#                myOut = facMap(barMap(myTens))
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
#f3.write("\n\\end{align*}")
#f2.close()
#f3.close()