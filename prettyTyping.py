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
        if inum % numPerLine == numPerLine - 1:
            if not (inum == len(lst) -1):
                print '\\) \n \n \\('
    print '\\)'
def latexOpen():
    print "\\documentclass[11pt, oneside]{article}   	% use \"amsart\" instead of \"article\" for AMSLaTeX format"
    print "\\usepackage{geometry}                		% See geometry.pdf to learn the layout options. There are lots."
    print "\\geometry{a4paper}                   		% ... or a4paper or a5paper or ... "
    print "%\\geometry{landscape}                		% Activate for for rotated page geometry"
    print "%\\usepackage[parfill]{parskip}    		% Activate to begin paragraphs with an empty line rather than an indent"
    print "\\usepackage{MyThesis}"
    print "\\begin{document}"
def latexClose():
    print "\\end{document}"

