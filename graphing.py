import networkx as nx
import matplotlib.pyplot as plt

from polynomial import polynomial
from monomial import monomial
from coefficient import coefficient
from pureTensor import pureTensor
from tensor import tensor
import copy
import re
from chainMaps import barMap


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



def mono(vs=[],c=coefficient()):
    return monomial(vs,symbs,rels,c)
x1 = mono(["x1"])
x2 = mono(["x2"])
x3 = mono(["x3"])
x4 = mono(["x4"])
zero = mono([],coefficient({'':0}))
one = mono()

colours = ["red","blue","green","beige","cyan","darkgreen"]
G=nx.DiGraph()



#note this function assumes the variable you give it already has a node associated to it!
def makeGraph(x):
   # print "makeGraph 1 debug",x
    assert isinstance(x,monomial)
    if x.sorted():
      #  print "makeGraph exitclause debug"
        return
    else:
        for r in rels:
           # print r, "makeGraph r debug",rels[r]
            for inum,i in enumerate(x.vs):
               # print inum,"makeGraph inum debug"
                if inum == len(x.vs)-1:
                    break
                else:
                   # print "else clause debug"
                    if x.vs[inum]==r[0] and x.vs[inum+1]==r[1]:
                        newvs = copy.deepcopy(x.vs)
                        tempMono = mono(newvs[:inum]+rels[r]+newvs[inum+2:])
                        #print tempMono, "tempMono debug"
                        G.add_node(tempMono.__repr__())
                        G.add_edge(x.__repr__(),tempMono.__repr__(),{'color': colours[inum]})
                        makeGraph(tempMono)
        return




x = x4*x1*x3*x2*x3*x1*x2
G.add_node(x.__repr__())
makeGraph(x)
#nx.spring_layout(G)
#edges,colors = zip(*nx.get_edge_attributes(G,'color').items())
#nx.draw(G,edgelist=edges,edge_color=colors,width=2)
#plt.savefig("graphing.png")


# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"
nx.write_dot(G,'test.dot')

# same layout using matplotlib with no labels
plt.title("draw_networkx")
pos=nx.graphviz_layout(G,prog='dot')
nx.draw(G,pos,with_labels=False,arrows=True)
plt.savefig('graphing.png')
nx.write_graphml(G,'so.graphml')

