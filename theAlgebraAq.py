from monomial import generators
from algebra import algebra
from vector import vector
from pureTensor import pureTensor
from relation import relation
from doublyDefined import doublyDefined
from coefficient import coefficient
from functionOnKn import functionOnKn
"""
File: theAlgebraAq.py
Author: Chris Campbell
Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
Github: https://github.com/chriscampbell19
Description: This file defines the algebra Aq, it's bases in degrees 0 - 3 and
bases of K1,K2,K3
"""
##############################################################################
######  Bases of homogeneous components
##############################################################################

x1, x2, x3, x4 = generators('x1 x2 x3 x4')
A1Basis = gens = [x2, x1, x3, x4]

A2Basis =[]
for index1,i in enumerate(gens):
    for index2, j in enumerate(gens):
        if index2 < index1:
            continue
        A2Basis.append(i * j)

A3Basis = []

for index1,i in enumerate(gens):
    for index2, j in enumerate(gens):
        if index2 < index1:
            continue
        for index3, k in enumerate(gens):
            if index3 < index2:
                continue
            A3Basis.append(i * j * k)

A4Basis = []

for index1,i in enumerate(gens):
    for index2, j in enumerate(gens):
        if index2 < index1:
            continue
        for index3, k in enumerate(gens):
            if index3 < index2:
                continue
            for index4, l in enumerate(gens):
                if index4 < index3:
                    continue
                A4Basis.append(i * j * k * l)
bases = [[1],gens,A2Basis,A3Basis,A4Basis]
##############################################################################
######  The Algebra Aq
##############################################################################
q = coefficient('q')
relations = [relation(x3 * x1, x1 * x3),
    relation(x4 * x2, x2 * x4 * q),
    relation(x4 * x1, x2 * x3),
    relation(x1 * x2, x2 * x3),
    relation(x3 * x2, x1 * x4 * q),
    relation(x4 * x3, x1 * x4)]
r = [0] + relations
Aq = algebra(relations)
##############################################################################
######  Koszul Complex Bases
##############################################################################

qK1Basis = []
for i in gens:
    qK1Basis.append(pureTensor([1,i,1]))
qK2Basis = []
for i in relations:
    qK2Basis.append(pureTensor([1,i,1]))

doublyDefineds = [ doublyDefined( [[x3,r[4]],[x1*q,r[6]],[-x1,r[5]]],[[r[1],x2],[r[5],-x3]]),
                  doublyDefined( [[x4,r[1]],[-x1,r[3]]],[[r[6],x1],[r[4],x3],[r[3],-x3]]),
                  doublyDefined( [[x4,r[5]],[-x1,r[2]]],[[r[6],x2],[r[4],q * x4],[r[3],-x4*q]]),
                  doublyDefined( [[x4,r[4]],[x2 * q,r[6]],[-x2,r[5]]],[[r[3],x2],[r[2],-x3]])]
dd = [0] + doublyDefineds
qK3Basis = [pureTensor([1,x,1]) for x in doublyDefineds]
qK4Bar =[ doublyDefined( [[x4,dd[1]],[-x1,dd[4]]],[[dd[2],x2],[dd[3],-x3]])]
qK4Basis = [pureTensor([1,x,1]) for x in qK4Bar]

qK1DualBasis = []
for i in A1Basis:
    qK1DualBasis.append( functionOnKn(Aq, qK1Basis,[i,0,0,0]))
for i in A1Basis:
    qK1DualBasis.append( functionOnKn(Aq, qK1Basis,[0,i,0,0]))
for i in A1Basis:
    qK1DualBasis.append( functionOnKn(Aq, qK1Basis,[0,0,i,0]))
for i in A1Basis:
    qK1DualBasis.append( functionOnKn(Aq, qK1Basis,[0,0,0,i]))
qK2DualBasis = []
for i in A2Basis:
    qK2DualBasis.append( functionOnKn(Aq, qK2Basis,[i,0,0,0,0,0]))
for i in A2Basis:
    qK2DualBasis.append( functionOnKn(Aq, qK2Basis,[0,i,0,0,0,0]))
for i in A2Basis:
    qK2DualBasis.append( functionOnKn(Aq, qK2Basis,[0,0,i,0,0,0]))
for i in A2Basis:
    qK2DualBasis.append( functionOnKn(Aq, qK2Basis,[0,0,0,i,0,0]))
for i in A2Basis:
    qK2DualBasis.append( functionOnKn(Aq, qK2Basis,[0,0,0,0,i,0]))
for i in A2Basis:
    qK2DualBasis.append( functionOnKn(Aq, qK2Basis,[0,0,0,0,0,i]))
qK3DualBasis = []
for i in A3Basis:
    qK3DualBasis.append( functionOnKn(Aq, qK3Basis, [i,0,0,0]))
for i in A3Basis:
    qK3DualBasis.append( functionOnKn(Aq, qK3Basis, [0,i,0,0]))
for i in A3Basis:
    qK3DualBasis.append( functionOnKn(Aq, qK3Basis, [0,0,i,0]))
for i in A3Basis:
    qK3DualBasis.append( functionOnKn(Aq, qK3Basis, [0,0,0,i]))
qK4DualBasis = []
for i in A4Basis:
    qK4DualBasis.append(functionOnKn(Aq,qK4Basis, [i]))

qHH2Basis = [ [ x1 * x3 , 0 , 0 , x2 * x3 , q *x1 * x4 , 0],
    [ 0 , x2 * x2 , 0 , 0 , x2 * x3 , 0 ],
    [ 0 , x2 * x4 , 0 , 0 , x1 * x4 , 0 ],
    [ 0 , x4 * x4 , 0 , 0 , x3 * x4 , 0 ]]

qHH2Basis = [functionOnKn(Aq, qK2Basis, vector(i)) for i in qHH2Basis]
if __name__ == '__main__':
    pass
