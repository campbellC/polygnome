import sys
sys.path.append("../")
import unittest
from pureTensor import pureTensor
from chainMaps import *
from theAlgebraA import A,bases,K2Basis,K3Basis,x2,x1,x4,x3
from theAlgebraAq import Aq,qK2Basis,qK3Basis
from functionOnKn import functionOnKn
from vector import vector
class chainMapsTest(unittest.TestCase):

    ##############################################################################
    ###### A tests
    ##############################################################################


    def test_Gerstenhaber1(self):
        f = functionOnKn(A,K2Basis, [0,0,0,x2*x3,0,-x1*x4])
        g = GerstenhaberBracket(f,f,K3Basis)
        answer = vector([2 * x1 * x1 * x4,-x2 * x3 * x3 * 2,-2 * x2 * x3 * x4,2 * x2 * x1 * x4])
        self.assertEqual(g,answer)

    def test_Gerstenhaber2(self):
        f = functionOnKn(A,K2Basis, [x1*x3,0,0,x2*x3,x1*x4,0])
        g = GerstenhaberBracket(f,f,K3Basis)
        answer = vector([0,0,0,0])
        self.assertEqual(g,answer)
