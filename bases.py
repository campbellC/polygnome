from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
import copy
import re
from chainMaps import barMap
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
########################################################################################################################################################################################################################
#################################### Here we generate the bases of K1, K2 and K3 in degree 1,2 and 3 respectively
########################################################################################################################################################################################################################
basisK1 = []
variables = [x2,x1,x3,x4]
for i in range(4):
    for j in range(4):
        vect = [zero] * 4
        vect[i] = vect[i] + variables[j]
        basisK1.append(vect)

basisK2 = []
for i in range(6):
    for j in range(4):
        for k in range(j,4):
            vect = [zero] * 6
            vect[i] = vect[i] + variables[j] * variables[k]
            basisK2.append(vect)

basisK3 = []
for i in range(4):
    for j in range(4):
        for k in range(j,4):
            for l in range(k,4):
                vect = [zero] * 4
                vect[i] = vect[i] + variables[j] * variables[k] * variables[l]
                basisK3.append(vect)
#
