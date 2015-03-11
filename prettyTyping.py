import re


xre = re.compile(r'([a-zA-Z])([\d]+)')

def vectToLatex(vect):
    print '\\left( \\begin{array}{c}'
    for i in vect:
        i = re.sub(xre, r'\1_\2', i.__repr__())
        print i , '\\\\'
    print '\\end{array} \\right)'



def listOfVectsToLatex(lst, numPerLine = 5): #this prints out numPerLine vectors in a row and then prints a new line and carries on. This does add \( and \) at beginning and end.
    print '\\( '
    for inum, i in enumerate(lst):
        vectToLatex(i)
        if inum % 5 == 4:
            print '\\) \n \n \\(' if not (inum == len(lst) - 1) else ''
    print '\\)'
