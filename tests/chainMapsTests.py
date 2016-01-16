import sys
sys.path.append("../")
import unittest
from pureTensor import pureTensor
from chainMaps import *
from theAlgebraA import A,bases,K2Basis,K3Basis


class chainMapsTest(unittest.TestCase):



    def test_diagramCommutesTestA1(self):
        TESTSET =[]
        for i in bases[2]:
            for j in bases[2]:
                TESTSET.append(pureTensor([1,i,j,1]))
        for i in TESTSET[:10]:
            self.assertEqual(k_2(m_2(i,A),A),m_1(b_n(i,A),A))

    def test_diagramCommutesTestA2(self):
        TESTSET = []
        for i in bases[2]:
            for j in bases[3]:
                TESTSET.append(pureTensor([1,i,j,1]))
                TESTSET.append(pureTensor([1,j,i,1]))
        for i in TESTSET[:10]:
            self.assertEqual(k_2(m_2(i,A),A),m_1(b_n(i,A),A))

    def test_diagramCommutesTestA3(self):
        TESTSET =[]
        for i in bases[3]:
            for j in bases[3]:
                TESTSET.append(pureTensor([1,i,j,1]))
        for i in TESTSET[:10]:
            self.assertEqual(k_2(m_2(i,A),A),m_1(b_n(i,A),A))

    def test_k_3_k_2_chainCondition(self):
        for i in K3Basis:
            self.assertEqual(k_2(k_3(i,A),A),0)

    def test_i_3_i_2_commutingCondition(self):
        for i in K3Basis:
            self.assertEqual(b_n(i_3(i,A),A),i_2(k_3(i,A),A))

    def test_i_2_i_1_commutingCondition(self):
        for i in K2Basis:
            self.assertEqual(b_n(i_2(i,A),A),i_1(k_2(i,A),A))

    # def test_diagramCommutesTestAq(self):
        # for i in self.TESTSET:
            # self.assertEqual(k_2(m_2(i,Aq),Aq),m_1(b_n(i,Aq),Aq))

