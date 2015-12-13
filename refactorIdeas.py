# one should define a function on pure Tensors with 1's on the outside. Then a factory should take this
# function and convert it into one that can handle polys on the outsidee, then
# finally another factory should make it additive
def ExtendMultpilicatively(f):
    def local(tens):
        assert isinstance(tens,pureTensor)
        ten = copy.deepcopy(tens)
        ten.sort()
        if not ten.monos[0].isNum():
            a = copy.deepcopy(ten.monos[0])
            ten.monos[0] = one
            return a * local(ten)
        elif not ten.monos[-1].isNum():
            b = copy.deepcopy(ten.monos[-1])
            ten.monos[-1] = one
            return local(ten) * b
        else:
            return f(ten)
    return local
def ExtendAdditively(f):
    def local(tens):
        assert isinstance(tens, pureTensor) or isinstance(tens, tensor)
        if isinstance(tens,pureTensor):
            return f(tens)
        else:
            tens.sort()
            if tens.ps == []:
                return f(pureTensor())
            ret = 0
            for inum, i in tens.ps:
                if inum == 0:
                    ret = f(i)
                else:
                    ret = ret + f(i)
            return ret
def BimoduleMap(f):
    return ExtendAdditively(ExtendMultpilicatively(f))


