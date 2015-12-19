from abc import ABCMeta, abstractmethod
import arithmeticInterface
class abstractTensor(arithmeticInterface.arithmeticInterface):
    __metaclass__ = ABCMeta
    """
    File: abstractTensor.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: An abstract class for elements of tensor product algebras.
    """
    @abstractmethod
    def __iter__(): pass
