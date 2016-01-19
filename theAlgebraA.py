from monomial import generators
from algebra import algebra
from vector import vector
from pureTensor import pureTensor
from relation import relation
from doublyDefined import doublyDefined
from functionOnKn import functionOnKn
"""
File: theAlgebraA.py
Author: Chris Campbell
Email: c (dot) j (dot)  campbell (at) ed (dot) ac (dot) uk
Github: https://github.com/chriscampbell19
Description: This file defines the algebra A, it's bases in degrees 0 - 3 and
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

bases = [[1],gens,A2Basis,A3Basis]
##############################################################################
######  The Algebra A
##############################################################################

relations = [relation(x3 * x1, x1 * x3),
            relation(x4 * x2, x2 * x4),
            relation(x4 * x1, x2 * x3),
            relation(x1 * x2, x2 * x3),
            relation(x3 * x2, x1 * x4),
            relation(x4 * x3, x1 * x4)]
r = [0] + relations
A = algebra(relations)
##############################################################################
######  Koszul Complex Bases
##############################################################################

K1Basis = []
for i in gens:
    K1Basis.append(pureTensor([1,i,1]))
K2Basis = []
for i in relations:
    K2Basis.append(pureTensor([1,i,1]))

doublyDefineds = [ doublyDefined( [[x3,r[4]],[x1,r[6]],[-x1,r[5]]],[[r[1],x2],[r[5],-x3]]),
                  doublyDefined( [[x4,r[1]],[-x1,r[3]]],[[r[6],x1],[r[4],x3],[r[3],-x3]]),
                  doublyDefined( [[x4,r[5]],[-x1,r[2]]],[[r[6],x2],[r[4],x4],[r[3],-x4]]),
                  doublyDefined( [[x4,r[4]],[x2,r[6]],[-x2,r[5]]],[[r[3],x2],[r[2],-x3]])]
K3Basis = [pureTensor([1,x,1]) for x in doublyDefineds]

K1DualBasis = []
for i in A1Basis:
    K1DualBasis.append( functionOnKn(A,K1Basis,[i,0,0,0]))
for i in A1Basis:
    K1DualBasis.append( functionOnKn(A,K1Basis,[0,i,0,0]))
for i in A1Basis:
    K1DualBasis.append( functionOnKn(A,K1Basis,[0,0,i,0]))
for i in A1Basis:
    K1DualBasis.append( functionOnKn(A,K1Basis,[0,0,0,i]))

K2DualBasis = []
for i in A2Basis:
    K2DualBasis.append( functionOnKn(A,K2Basis,[i,0,0,0,0,0]))
for i in A2Basis:
    K2DualBasis.append( functionOnKn(A,K2Basis,[0,i,0,0,0,0]))
for i in A2Basis:
    K2DualBasis.append( functionOnKn(A,K2Basis,[0,0,i,0,0,0]))
for i in A2Basis:
    K2DualBasis.append( functionOnKn(A,K2Basis,[0,0,0,i,0,0]))
for i in A2Basis:
    K2DualBasis.append( functionOnKn(A,K2Basis,[0,0,0,0,i,0]))
for i in A2Basis:
    K2DualBasis.append( functionOnKn(A,K2Basis,[0,0,0,0,0,i]))

K3DualBasis = []
for i in A3Basis:
    K3DualBasis.append( functionOnKn(A, K3Basis, [i,0,0,0]))
for i in A3Basis:
    K3DualBasis.append( functionOnKn(A, K3Basis, [0,i,0,0]))
for i in A3Basis:
    K3DualBasis.append( functionOnKn(A, K3Basis, [0,0,i,0]))
for i in A3Basis:
    K3DualBasis.append( functionOnKn(A, K3Basis, [0,0,0,i]))

HH2Basis = [[x1 * x3, 0, 0, x2 * x3, x1 * x4, 0],
    [ x3 * x3, 0, x1 * x4, 0, 0, x3 * x4],
    [ x1 * x1, 0, 0, x2 * x1, x2 * x3, 0],
    [ 0, x4 * x4, 0, 0, x3 * x4, 0],
    [ 0, x2 * x4, 0, 0, x1 * x4, 0],
    [ 0, x2 * x2, 0, 0, x2 * x3, 0],
    [ 0, 0, 0, x1 * x1, 0, x1 * x3*(-1)],
    [ 0, 0, 0, x2 * x2 * (-1), 0, x2 * x4] ]

HH2Basis = [functionOnKn(A,K2Basis,vector(vec)) for vec in HH2Basis]
if __name__ == '__main__':
    pass
