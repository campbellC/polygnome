import sys
sys.path.append("../")
import unittest
from pureTensor import pureTensor
from chainMaps import *
from algebrasOfInterest import A,Aq,bases


class chainMapsTest(unittest.TestCase):

    def setUp(self):
        self.TESTSET =[]
        for i in bases[2]:
            for j in bases[2]:
                self.TESTSET.append(pureTensor([1,i,j,1]))
        for i in bases[2]:
            for j in bases[3]:
                self.TESTSET.append(pureTensor([1,i,j,1]))
                self.TESTSET.append(pureTensor([1,j,i,1]))

        for i in bases[3]:
            for j in bases[3]:
                self.TESTSET.append(pureTensor([1,i,j,1]))

    def test_diagramCommutesTestA(self):
        for i in self.TESTSET:
            self.assertEqual(k_2(m_2(i,A),A),m_1(b_n(i,A),A))

    def test_diagramCommutesTestAq(self):
        for i in self.TESTSET:
            self.assertEqual(k_2(m_2(i,Aq),Aq),m_1(b_n(i,Aq),Aq))

