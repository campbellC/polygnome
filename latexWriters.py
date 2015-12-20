def listOfObjectsToLatex(lst, numPerLine=5): #this prints out numPerLine vectors in a row and then prints a new line and carries on. This does add \( and \) at beginning and end.
    print '\\( '
    for inum, i in enumerate(lst):
        print i.toLatex()
        if inum % numPerLine == numPerLine - 1:
            if not (inum == len(lst) -1):
                print '\\) \n \n \\('
    print '\\)'

def latexOpen():
    print '\\documentclass[11pt, oneside]{report}'
    print '\\usepackage{MyThesis}'
    print '\\begin{document}'

def latexClose():
    print "\\end{document}"
