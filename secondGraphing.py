
import pdb
from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
from pureTensor import pureTensor
from tensor import tensor
import copy
import re
from chainMaps import barMap
import itertools
globalFlag = False


symbs = ["x1", "x2","x3","x4"]
rels = { ("x3" ,"x1") : ["x1", "x3"],\
    ("x4", "x2") : ["x2", "x4"],\
    ("x4", "x1") : ["x2", "x3"],\
    ("x1", "x2") : ["x2", "x3"],\
    ("x3", "x2") : ["x1", "x4"],\
    ("x4", "x3") : ["x1", "x4"]}

r = {1: {("x3" ,"x1") : ["x1", "x3"]},\
    2: {("x4", "x2") : ["x2", "x4"]},\
    3: {("x4", "x1") : ["x2", "x3"]},\
    4:{("x1", "x2") : ["x2", "x3"]},\
    5:{("x3", "x2") : ["x1", "x4"]},\
    6:{("x4", "x3") : ["x1", "x4"]} }


def mono(vs,c=coefficient()):
    return monomial(vs,symbs,rels,c)
x1 = mono(["x1"])
x2 = mono(["x2"])
x3 = mono(["x3"])
x4 = mono(["x4"])
zero = mono([],coefficient({'':0}))
one = mono([])


findAllPathsmemoIsation={}
def findAllPaths(x):
    if tuple(x.vs) in findAllPathsmemoIsation:
        return findAllPathsmemoIsation[tuple(x.vs)]
    
    assert isinstance(x,monomial)
    if x.sorted():
        findAllPathsmemoIsation[tuple(x.vs)] = []
        return []
    ret = []
    for r in rels:
        #print r, "findAllPaths r debug",rels[r]
        for inum,i in enumerate(x.vs):
            #print inum,"findAllpaths inum debug"
            if inum == len(x.vs)-1:
                break
            else:
                if x.vs[inum]==r[0] and x.vs[inum+1]==r[1]:
#print "if debug findAllPaths",x,r,inum
                    newvs = copy.deepcopy(x.vs)
                    tempMono = mono(newvs[:inum]+rels[r]+newvs[inum+2:])
                    #print "debug tempMono", tempMono
                    recur = findAllPaths(tempMono)
                    if recur == []:
                        ret += [[[x,inum]]]
                    else:
                        for path in recur:
                            ret+= [[[x,inum]]+path]
                    #print x,ret, "ret debug"
    findAllPathsmemoIsation[tuple(x.vs)] = ret
    return ret





def splitCount(p1,p2,splitcount = 0):#calculates how many times two paths split up
    if len(p1)==0 or len(p2)==0: #if either path is empty then the recursion has finished
        return splitcount
    if p1[0][0].vs==p2[0][0].vs and p1[0][1]==p2[0][1]: #if the paths agree just recurse down both
        return splitCount(p1[1:],p2[1:],splitcount)
    elif p1[0][0].vs==p2[0][0].vs: #if the paths start at the same point, but diverge then record a split and recurse
        return splitCount(p1[1:],p2[1:],splitcount+1)
    else:
        for inum,i in enumerate(p1):
            for jnum,j in enumerate(p2):
                if p1[inum][0].vs == p2[jnum][0].vs:
                    return splitCount(p1[inum:],p2[jnum:],splitcount)
        return splitcount
    

#

def meetingPoint(p1,p2):#assumes you start at DIFFERENT nodes
            for inum,i in enumerate(p1):
                for jnum,j in enumerate(p2):
                    if i[0].vs == j[0].vs:
                        return (inum,jnum)
            else:
                return False
            
def splittingPoint(p1,p2,point = 0):#this assumes splitcount = 1 
            if p1[0][0].vs==p2[0][0].vs and p1[0][1]==p2[0][1]: #if the paths agree just recurse down both
                return splittingPoint(p1[1:],p2[1:],point+1)
            elif p1[0][0].vs==p2[0][0].vs and p1[0][1]!=p2[0][1]: 
                return point
            
            
def differByACP(p1,p2): #returns False if not, -1 if p1 is to the left of p2, 1 if vice versa
    if splitCount(p1,p2) != 1:
        return False
    else:
        splitPoint = splittingPoint(p1,p2)
        col1 = p1[splitPoint][1]
        col2 = p2[splitPoint][1]
        meetPoints = meetingPoint(p1[splitPoint+1:],p2[splitPoint+1:])
        if meetPoints:
            point1 = meetPoints[0]+splitPoint+1
            point2 = meetPoints[1]+splitPoint+1
        else:
            point1 = len(p1)
            point2 = len(p2)
        for i in p1[splitPoint:point1]:
            if i[1]!= col1 and i[1]!=col2:
                return False
        for i in p2[splitPoint:point2]:
            if i[1]!= col1 and i[1]!=col2:
                return False
        return 1 if col1<col2 else -1




def K3FromACPDifferingPaths(p1,p2):#from right to left, so assumes p1 is left of p2!!!!!!
    ACP = differByACP(p1,p2)
    if not ACP:
        raise NameError("Tried K3FromPathsACPDifferingPaths on two paths not differing by ACP")
    splitPoint = splittingPoint(p1,p2)
    col1 = p1[splitPoint][1]
    col2 = p2[splitPoint][1]
    if abs(col1 - col2) > 1:
        return tensor([])
    meetPoints = meetingPoint(p1[splitPoint+1:],p2[splitPoint+1:])
    if meetPoints:
        point1 = meetPoints[0]+splitPoint+1
        point2 = meetPoints[1]+splitPoint+1
    else:
        point1 = len(p1)
        point2 = len(p2)
    answer = tensor([])
    if col1 < col2:
        col = col2
        jnum = 0
        inum = 1
    else:
        col = col1
        jnum = 1
        inum = 0
    
    p1 = p1[splitPoint:point1]
    p2 = p2[splitPoint:point2]
    while inum<len(p1):
        variableList = p1[inum][0].vs
        r = (variableList[col] , variableList[col+1])
        answer += pureTensor([mono(variableList[:col-1]),mono([variableList[col-1]]),\
                              {r : rels[r]},mono(variableList[col+2:])]) * ACP * -1
        inum +=2
    while jnum<len(p2):
        variableList = p2[jnum][0].vs
        r = (variableList[col] , variableList[col+1])
        answer += pureTensor([mono(variableList[:col-1]),mono([variableList[col-1]]),\
                              {r : rels[r]},mono(variableList[col+2:])]) * ACP 
        jnum += 2
    return answer
    
    


def pathEqual(p1,p2):
    if len(p1)!= len(p2):
        return False
    else:
        for inum,i in enumerate(p1):
            if i[1]!= p2[inum][1]:
                return False
        return True
            

def find2Path(p1,p2,pathToHere=[]): #find a path between simp-paths by brute force recursion from p2 to p1

    pathToHere = pathToHere+ [p2]
    if pathEqual(p1,p2):
        return pathToHere
    elif differByACP(p1,p2):
        return pathToHere + [p1]
    else:
        allPaths = findAllPaths(p1[0][0])
        
        for p3 in allPaths:
            
            
            if differByACP(p2,p3) == -1:
                for i in pathToHere:
                    if pathEqual(i,p3):
                        break
                else:
                    
                    
                    answer = find2Path(p1,p3,pathToHere)
                    if answer:
                        return answer
        for p3 in allPaths:
            if differByACP(p2,p3) == 1:
                
                for i in pathToHere:
                    if pathEqual(i,p3):
                        break
                else:
                    answer = find2Path(p1,p3,pathToHere)
                    if answer:
                        return answer
        return False
                    
        
    
       

def K3FromTwoPaths(p1,p2):
    global globalFlag
    findAllPathsmemoIsation={}
    answer = tensor([])
    if pathEqual(p1,p2):
        return tensor([])
    path = find2Path(p1,p2)
    for inum,i in enumerate(path):
        if inum == len(path)-1:
            continue
        else:
            if differByACP(path[inum],path[inum+1]) == 1:
                globalFlag = True
                
            answer += K3FromACPDifferingPaths(path[inum],path[inum+1])
    return answer
    
        
        
def Lpath(abc):
    answer =[]
    for i in abc.facSeq():
        answer.append([i[0],i[1]])
    return answer

def splitIntoMonomials(abc):#returns a list of longest pbw submonomials
    for inum in range(len(abc.vs)):
        if mono(abc.vs[:inum]).sorted() and not mono(abc.vs[:inum+1]).sorted():
            return [mono(abc.vs[:inum])] + splitIntoMonomials(mono(abc.vs[inum:]))
    return [abc]


def RLpath(abc):
    answer = []
    abc = splitIntoMonomials(abc)
    a=abc[0]
    bc = abc[1]*abc[2]
    for i in bc.facSeq():
        answer.append([a*i[0],i[1]+a.degree()]) #possible off by one error
    bc.sort()
    abc = a*bc
    for i in abc.facSeq():
        answer.append([i[0],i[1]])
    return answer
def M3(tens):
    assert isinstance(tens,pureTensor) or isinstance(tens,tensor)
    ten = copy.deepcopy(tens)
    ret = copy.deepcopy(tens)
   
    if isinstance(ten,tensor):
        flag = True
        for i in ten.ps:
            if flag:
                ret = M3(i)
                flag = False
            else:
                ret = ret + M3(i)
            
    if isinstance(ten,pureTensor):
        assert tens.degree() == 5
        if not ten.monos[0].isNum():
            a = copy.deepcopy(ten.monos[0])
            ten.monos[0].vs = []
            return a * M3(ten)
        elif not ten.monos[4].isNum():
            b = copy.deepcopy(ten.monos[4])
            ten.monos[4].vs = []
            return M3(ten) * b
        else:
            abc = ten.monos[1]*ten.monos[2]*ten.monos[3]
            return K3FromTwoPaths(Lpath(abc),RLpath(abc))
        



ys1=[x2,x1,x3,x4]
xs=[x2,x1,x3,x4]
for inum,i in enumerate(ys1):
    for jnum,j in enumerate(ys1):
        for knum,k in enumerate(ys1):
            if inum <= jnum:
                xs.append(i*j)
            if inum <= jnum and jnum <=knum:
                xs.append(i*j*k)
                
  
f1 = open("/Data/OutputOfm3Test2.txt",'w')      
for inum,i in enumerate(xs):
    #print inum, "Outer Loop debug"
    for jnum,j in enumerate(xs):
        for knum,k in enumerate(xs):
            if (i*j).sorted() or (j*k).sorted():
                #print i,j,k,"if clause debug"
                continue
            else:
                
                
                myTens = pureTensor([one,i,j,k,one])
            #print myTens,"------>",barMap(myTens)

                myOut = M3(myTens)
                
                if globalFlag:
                    global globalFlag
                    globalFlag = False
                    myOut.sort()
                    f1.write("1|"+i.__repr__()+"|"+j.__repr__()+"|"+k.__repr__()+"|1 --> ")
                    line = myOut.__repr__()
                    line = re.sub(r"\-\->",r"&\\mapsto",re.sub(r"x",r"x_",line))
                    line = re.sub(r"{\('x_3', 'x_1'\): \['x_1', 'x_3'\]}",r"r_1",line)
                    line = re.sub(r"{\('x_4', 'x_2'\): \['x_2', 'x_4'\]}",r"r_2",line)
                    line = re.sub(r"{\('x_4', 'x_1'\): \['x_2', 'x_3'\]}",r"r_3",line)
                    line = re.sub(r"{\('x_1', 'x_2'\): \['x_2', 'x_3'\]}",r"r_4",line)
                    line = re.sub(r"{\('x_3', 'x_2'\): \['x_1', 'x_4'\]}",r"r_5",line)
                    line = re.sub(r"{\('x_4', 'x_3'\): \['x_1', 'x_4'\]}",r"r_6",line)
                    
                    f1.write(line+"\n")    
            


f1.close()
#f2 = open("OutputOfm3Test2.txt",'r')
#f3 = open("latexOutputm3Test2.txt",'w')
#f3.write("\\begin{align*}\n")
#for line in f2:
#    if line == "":
#        continue
#    line = re.sub(r"\-\->",r"&\\mapsto",re.sub(r"x",r"x_",line))
#    line = re.sub(r"{\('x_3', 'x_1'\): \['x_1', 'x_3'\]}",r"r_1",line)
#    line = re.sub(r"{\('x_4', 'x_2'\): \['x_2', 'x_4'\]}",r"r_2",line)
#    line = re.sub(r"{\('x_4', 'x_1'\): \['x_2', 'x_3'\]}",r"r_3",line)
#    line = re.sub(r"{\('x_1', 'x_2'\): \['x_2', 'x_3'\]}",r"r_4",line)
#    line = re.sub(r"{\('x_3', 'x_2'\): \['x_1', 'x_4'\]}",r"r_5",line)
#    line = re.sub(r"{\('x_4', 'x_3'\): \['x_1', 'x_4'\]}",r"r_6",line)
#    f3.write(line+"\\\\")
#f3.write("\\end{align*}")
#f2.close()
#f3.close()

#
##note this function assumes the variable you give it already has a node associated to it!
#def makeGraph(x):
#   # print "makeGraph 1 debug",x
#    assert isinstance(x,monomial)
#    if x.sorted():
#      #  print "makeGraph exitclause debug"
#        return
#    else:
#        for r in rels:
#           # print r, "makeGraph r debug",rels[r]
#            for inum,i in enumerate(x.vs):
#               # print inum,"makeGraph inum debug"
#                if inum == len(x.vs)-1:
#                    break
#                else:
#                   # print "else clause debug"
#                    if x.vs[inum]==r[0] and x.vs[inum+1]==r[1]:
#                        newvs = copy.deepcopy(x.vs)
#                        tempMono = mono(newvs[:inum]+rels[r]+newvs[inum+2:])
#                        #print tempMono, "tempMono debug"
#                        G.add_node(tempMono.__repr__())
#                        G.add_edge(x.__repr__(),tempMono.__repr__(),{'Color': colours[inum]})
#                        makeGraph(tempMono)
#        return
#
#
#
#
#m = z*y*x*w
#G.add_node(m.__repr__())
#makeGraph(m)
##nx.spring_layout(G)
##edges,colors = zip(*nx.get_edge_attributes(G,'color').items())
##nx.draw(G,edgelist=edges,edge_color=colors,width=2)
##plt.savefig("graphing.png")
#
#
## write dot file to use with graphviz
## run "dot -Tpng test.dot >test.png"
#nx.write_dot(G,'test.dot')
#
## same layout using matplotlib with no labels
#plt.title("draw_networkx")
#pos=nx.graphviz_layout(G,prog='dot')
#nx.draw(G,pos,with_labels=True,arrows=True)
#plt.savefig('graphing.png')
#nx.write_graphml(G,'so.graphml')
#
##