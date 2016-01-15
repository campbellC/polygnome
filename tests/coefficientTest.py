import sys
sys.path.append("../")
import unittest
from coefficient import coefficient

class coefficientTest(unittest.TestCase):
    def test_equality_with_numbers1(self):
        c = coefficient()
        self.assertEqual(c,1)

    def test_equality_with_numbers2(self):
        c = coefficient()
        self.assertEqual(c,1.0)

    def test_equality_with_numbers3(self):
        c = coefficient(0)
        self.assertEqual(c,0)

    def test_equality_with_numbers4(self):
        c = coefficient(-1500)
        self.assertEqual(c,-1500)

    def test_addition_with_numbers1(self):
        c = coefficient(1500)
        self.assertEqual(c-1500,0)

    def test_addition_with_numbers2(self):
        c = coefficient(1500)
        self.assertEqual(c+1500,3000)

    def test_addition_with_numbers3(self):
        c = coefficient(-1500)
        self.assertEqual(c+0,-1500)

    def test_multiplication_with_numbers1(self):
        c = coefficient(1)
        self.assertEqual(c * 1,1)

    def test_multiplication_with_numbers2(self):
        c = coefficient(1)
        self.assertEqual(c * 2,2)

    def test_multiplication_with_numbers3(self):
        c = coefficient(1)
        self.assertEqual(c * -2,-2)

    def test_addition_between_coefficients1(self):
        c1 = coefficient(1)
        c2 = coefficient(2)
        self.assertEqual(c1 + c2, 3)

    def test_addition_between_coefficients2(self):
        c1 = coefficient(1)
        c2 = coefficient(-2)
        self.assertEqual(c1 + c2, -1)

    def test_addition_between_coefficients3(self):
        c1 = coefficient(1)
        c2 = coefficient('q')
        c = coefficient({'':1,'q':1})
        self.assertEqual(c1 + c2, c)

