from abc import ABCMeta, abstractmethod

class polygnomeObject(object):
    __metaclass__ = ABCMeta

    """
    File: printableObject.py
    Author: Chris Campbell
    Email: c (dot) j (dot) campbell (at) ed (dot) ac (dot) uk
    Github: https://github.com/chriscampbell19
    Description: An abstract superclass that every object must inherit from. Outlines basic methods
    every polygnome class must have.
    """

    @abstractmethod
    def __repr__(self): pass #for printing within python

    @abstractmethod
    def toLatex(self): pass #so that every object will know how to output it's own latex representation



