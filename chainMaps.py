import pureTensor
import tensor
import monomial
import polynomial
import copy
import coefficient
import time

def barMap(tens):#for now assume this is above position 2, so the result is also a tensor
    ten = copy.deepcopy(tens)
    ret = copy.deepcopy(tens)
    ten.sort()
    if isinstance(ten,pureTensor.pureTensor):
        assert len(ten.monos) > 1
        for i in range(0,len(ten.monos)-1):
            temp = ten.monos[i]*ten.monos[i+1]
            if i == 0:
                ret = pureTensor.pureTensor([temp] + ten.monos[2:],ten.coeff * pow(-1,i))
            elif i == len(ten.monos) -2:
                ret = ret + (pureTensor.pureTensor(ten.monos[:i] + [temp],ten.coeff * pow(-1,i)))
            else:
                ret = ret + (pureTensor.pureTensor(ten.monos[:i]+[temp]+ten.monos[i+2:], ten.coeff* pow(-1,i)))
                        
    if isinstance(ten,tensor.tensor):
        flag = True
        for i in ten.ps:
            if flag:
                ret = barMap(i)
                flag = False
            else:
                ret = ret + barMap(i)
    return ret

def k2(tens):
    assert isinstance(tens,tensor.tensor) or isinstance(tens,pureTensor.pureTensor)
    ten = copy.deepcopy(tens)
    ret = copy.deepcopy(tens)
    if isinstance(ten,pureTensor.pureTensor):
        assert isinstance(ten.monos[1],dict)
        for i in ten.monos[1]:
            ###### a's
            a = copy.deepcopy(ten.monos[0])
            a.vs = a.vs + [i[0]]
            a1= copy.deepcopy(ten.monos[0])
            a1.vs = a1.vs + [ten.monos[1][i][0]]
            a2 = copy.deepcopy(ten.monos[0])
            a3 = copy.deepcopy(ten.monos[0])
            ###### b's
            b = copy.deepcopy(ten.monos[2])
            b1  = copy.deepcopy(ten.monos[2])
            b2 = copy.deepcopy(ten.monos[2])
            b2.vs = [i[1]] + b2.vs
            b3  = copy.deepcopy(ten.monos[2])
            b3.vs = [ten.monos[1][i][1]] + b3.vs
            #######c's
            c = copy.deepcopy(ten.monos[0])
            c.vs = [i[1]]
            c.coeff = coefficient.coefficient()
            c1 = copy.deepcopy(ten.monos[0])
            c1.vs = [ten.monos[1][i][1]]
            c1.coeff = coefficient.coefficient()* pow(-1,1)
            c2 = copy.deepcopy(ten.monos[0])
            c2.vs = [i[0]]
            c2.coeff = coefficient.coefficient() 
            c3 = copy.deepcopy(ten.monos[0])
            c3.vs = [ten.monos[1][i][0]]
            c3.coeff = coefficient.coefficient()* pow(-1,1)
            ret = pureTensor.pureTensor([a,c,b])
            ret = ret + pureTensor.pureTensor([a1,c1,b1])
            ret = ret + pureTensor.pureTensor([a2,c2,b2])
            ret = ret + pureTensor.pureTensor([a3,c3,b3])
            ret.sort()
    if isinstance(ten,tensor.tensor):
        flag = True
        for i in ten.ps:
            if flag:
                ret = k2(i)
                flag = False
            else:
                ret = ret + k2(i)
            ret.sort()
    return ret

    
    
    
def m1(tens):
    assert isinstance(tens,pureTensor.pureTensor) or isinstance(tens,tensor.tensor)
    ten = copy.deepcopy(tens)
    ten.sort()
    ret = copy.deepcopy(tens)
    if isinstance(tens,pureTensor.pureTensor):
        assert tens.degree() == 3
        if not ten.monos[0].isNum():
            a = copy.deepcopy(ten.monos[0])
            ten.monos[0].vs = []
            return a * m1(ten)
        elif not ten.monos[2].isNum():
            b = copy.deepcopy(ten.monos[2])
            ten.monos[2].vs = []
            return m1(ten) * b
        else:
            for i in range(0,len(ten.monos[1].vs)):
                a = copy.deepcopy(ten.monos[1])
                a.vs = ten.monos[1].vs[0:i]
                b = copy.deepcopy(ten.monos[1])
                b.vs = [ten.monos[1].vs[i]]
                c = copy.deepcopy(ten.monos[1])
                c.vs = ten.monos[1].vs[i+1:]
                if i ==0:
                    ret = pureTensor.pureTensor([a,b,c],ten.coeff)
                    assert isinstance(ret,pureTensor.pureTensor)
                    for i in ret.monos:
                        assert isinstance(i,monomial.monomial)
                else:
                    ret = ret + pureTensor.pureTensor([a,b,c],ten.coeff)
                ret.sort()
    if isinstance(ten,tensor.tensor):
        flag = True
        for i in ten.ps:
            if flag:
                ret = m1(i)
                flag = False
            else:
                ret = ret + m1(i)
            ret.sort()
    return ret
        
        
        
###########################################################################################################################################################
############################################################## EXPERIMENTS #############################################################################################
###########################################################################################################################################################



def facMap(tens):
    assert isinstance(tens,pureTensor.pureTensor) or isinstance(tens,tensor.tensor)
    ten = copy.deepcopy(tens)
    ret = copy.deepcopy(tens)
   
    if isinstance(ten,tensor.tensor):
        flag = True
        for i in ten.ps:
            if flag:
                ret = facMap(i)
                flag = False
            else:
                ret = ret + facMap(i)
            
    if isinstance(ten,pureTensor.pureTensor):
        assert tens.degree() == 4
        if not ten.monos[0].isNum():
            a = copy.deepcopy(ten.monos[0])
            ten.monos[0].vs = []
            return a * facMap(ten)
        elif not ten.monos[3].isNum():
            b = copy.deepcopy(ten.monos[3])
            ten.monos[3].vs = []
            return facMap(ten) * b
        else:
            x = tens.monos[1] * tens.monos[2]
            ret = tensor.tensor([])
            flag = True
            for i in x.facSeq():
                m = i[0]
                j = i[1]
                r = i[2]
                a = copy.deepcopy(m)
                a.vs = a.vs[:j]
                b = copy.deepcopy(m)
                b.vs = b.vs[j+2:]
                if flag:
                    ret = tensor.tensor([pureTensor.pureTensor([a,r,b])])
                    flag = False
                else:
                    ret = ret + pureTensor.pureTensor([a,r,b])
                
    ret.sort()
    return ret
            
            




























        
