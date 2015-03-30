import operator
from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
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
#################################### In this section we define k1, k2 and k3 the dual maps to the chain maps of the Koszul complex
########################################################################################################################################################################################################################

def k1(vect): 
    """This map takes a vector of 4 elements of A and returns a vector of six elements of A i.e. how it acts on the four basis vectors of K_1 and returns how it acts on the six basis vectors of K_2, the 4 vector takes x1 to the first, x2 to the second etc"""
    vect = ["placeholder"] + vect #this means that x[1] is what vect sends x1 to, x[2] is what vect sends x[2] to etc.
    return [  x3*vect[1] - x1* vect[3] + vect[3] * x1 - vect[1] * x3, \
              x4*vect[2] - x2* vect[4] + vect[4] * x2 - vect[2] * x4, \
              x4*vect[1] - x2* vect[3] + vect[4] * x1 - vect[2] * x3, \
              x1*vect[2] - x2* vect[3] + vect[1] * x2 - vect[2] * x3, \
              x3*vect[2] - x1* vect[4] + vect[3] * x2 - vect[1] * x4, \
              x4*vect[3] - x1* vect[4] + vect[4] * x3 - vect[1] * x4] 



def k2(vect): 
    """this takes a vector of six elements, which are the images of the 6 basis vectors of K_2 (i.e. the relations) and returns a vector of six elements which is where the 4 doubly defined relations go."""
    vect = ["placeholder"] + vect #this means that vect[1] is what vect sends r1 to
    return [ x3 * vect[4] + x1 * vect[6] - x1 * vect[5] - vect[1]*x2 + vect[5] * x3,\
             x4 * vect[1] - x1 * vect[3] - vect[6] * x1 - vect[4]*x3 + vect[3] * x3,\
             x4 * vect[5] - x1 * vect[2] - vect[6] * x2  - vect[4]*x4 + vect[3] * x4,\
             x4 * vect[4] + x2 * vect[6] - x2 * vect[5] - vect[3]*x2 + vect[2] * x3]

def k3(vect):
    """Takes a vector of four elements in A, which are the images of the doubly defined relations under that vector, and returns the image of the only triply defined relation"""
    vect = ["placeholder"] + vect
    return [x4 * vect[1] - x1 * vect[4] + vect[2] * x2 - vect[3] * x3]


