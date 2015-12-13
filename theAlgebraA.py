from coefficient import coefficient
from monomial import monomial
from generator import generator
from relation import relation
import abstractPolynomial
from algebra import algebra


x1 = generator('x1')
x2 = generator('x2')
x3 = generator('x3')
x4 = generator('x4')


r1 = relation(x3 * x1, x1 * x3)
r2 = relation(x4 * x2, x2 * x4)
r3 = relation(x4 * x3, x1 * x4)
r4 = relation(x1 * x2, x2 * x3)
r5 = relation(x4 * x1, x2 * x3)
r6 = relation(x3 * x2, x1 * x4)


A = algebra((r1,r2,r3,r4,r5,r6))
x1,x2,x3,x4 = A.canonicalProjection(x1),A.canonicalProjection(x2),A.canonicalProjection(x3),A.canonicalProjection(x4)
