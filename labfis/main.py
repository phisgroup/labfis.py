from math import floor, ceil, trunc, log, log10, sqrt
from numbers import Number

class LabFloatError(Exception):
    def __init__(self, *args):
        if args:
            if args[0] == 0:
                self.message = "Essa operação não é suportado nesta classe, apenas as operações mencionadas na apostila de Laboratório de Física 2 do IFSC."
            elif args[0] == 1:
                self.message = "Too many args in list, expected '[...,[val,err],...]' got '{0}'".format(args[1])
            elif isinstance(args[0],str):
                self.message = "{0}{1}".format(args[0],args[1])
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'LabFloatError has been raised'

class labfloat:
    def __init__(self, *args, **kwargs):
        mean = kwargs.get('mean',0.0)
        uncertainty = kwargs.get('uncertainty',0.0)

        if args:
            if len(args) == 1:
                mean = args[0]
            elif len(args) == 2:
                mean = args[0]
                uncertainty = args[1]
            else:
                raise LabFloatError("Too many arguments, expected (val,err) or ([(val,err),...]), got: ",args)

        self.mean = float(mean)
        self.uncertainty = abs(float(uncertainty))

    @classmethod
    def list(cls,listargs):
        listlabfloat = []
        for j in range(len(listargs)):
            if len(listargs[j]) == 2:
                listlabfloat += [cls(listargs[j][0],listargs[j][1])]
            elif len(listargs[j]) == 1:
                listlabfloat += [cls(listargs[j][0])]
            elif len(listargs[j]) > 2:
                raise LabFloatError(1,listargs[j])
        return(listlabfloat)

    def format(self):
        su = "%.16f" % self.uncertainty
        i = su.find(".")
        if i == -1:
            r = - len(su) + 1
            m = round(self.mean, r)
            u = round(self.uncertainty, r)
            return((m,u))
        else:
            r = -i
            r += 1
            for j in range(len(su)):
                if su[j] == "0":
                    r += 1
                elif su[j+1] == "9" and r > 0:
                    m = round(self.mean, r-1)
                    u = round(self.uncertainty, r)
                    return((m,u))
                elif su[j] != ".":
                    m = round(self.mean, r)
                    u = round(self.uncertainty, r)
                    return((m,u))

        m = round(self.mean, r)
        u = round(self.uncertainty, r)
        return((m,u))

    def split(self):
        if self.uncertainty == 0:
            return(["{:g}".format(self.mean)])
        else:
            m, u = self.format()
            return(["{:g}".format(m),"{:g}".format(u)])
          
    def tex(self,*args,**kwargs):
        precision = kwargs.get('precision')
        if args:
            if len(args) == 2:
                precision = args
            elif len(args) > 2:
                raise LabFloatError("Too many arguments, expected: (precision) or (mean precision,err precision) got: ",args)
            else:
                precision = [args[0],args[0]]

        if self.uncertainty == 0:
            if precision:
                precision[0] = str(precision[0])
                m = eval("'{:."+precision[0]+"e}'.format(self.mean)")
            else:
                m = self.split()[0]
            m = m.split("e")
            if len(m) > 1:
                m = m[0]+r"\cdot 10^{"+m[1]+"}"
            else:
                m = m[0]
            return("{0}".format(m))
        else:
            if precision:
                precision = (str(precision[0]),str(precision[1]))
                m, u = self.format()
                m = eval("'{:."+precision[0]+"e}'.format(m)")
                u = eval("'{:."+precision[1]+"e}'.format(u)")
            else:
                m, u = self.split()
            m = m.split("e")
            u = u.split("e")
            if len(m) > 1:
                m = m[0]+r"\cdot 10^{"+m[1]+"}"
            else:
                m = m[0]
            if len(u) > 1:
                u = u[0]+r"\cdot 10^{"+u[1]+"}"
            else:
                u = u[0]
            return(r"({0}\, \pm \,{1})".format(m, u))

    def __str__(self):
        val = self.split()
        if len(val) == 1:
            return("{0}".format(val[0]))
        else:
            return("({0} ± {1})".format(*val))

    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, idx):
        vals = [self.mean,self.uncertainty]
        return vals[idx]

    def __pos__(self):
        return self

    def __neg__(self):
        return labfloat(-self.mean, self.uncertainty)

    def __abs__(self):
        return labfloat(abs(self.mean), self.uncertainty)

    def __round__(self, n):
        return labfloat(round(self.mean, n), round(self.uncertainty, n))

    def __floor__(self):
        return labfloat(floor(self.mean), floor(self.uncertainty))

    def __ceil__(self):
        return labfloat(ceil(self.mean), ceil(self.uncertainty))

    def __trunc__(self):
        return labfloat(trunc(self.mean), trunc(self.uncertainty))

    def __eq__(self, other):
        if isinstance(other, labfloat):
            return abs(self.mean - other.mean) < 2 * (self.uncertainty + other.uncertainty)
        if isinstance(other, Number):
            return abs(self.mean - other) < 2 * self.uncertainty

    def __ne__(self, other):
        if isinstance(other, labfloat):
            return abs(self.mean - other.mean) > 3 * (self.uncertainty + other.uncertainty)
        if isinstance(other, Number):
            return abs(self.mean - other) > 3 * self.uncertainty

    def __lt__(self,other):
        if isinstance(other, labfloat):
            return self.mean + self.uncertainty < other.mean - other.uncertainty
        if isinstance(other, Number):
            return self.mean + self.uncertainty < other

    def __gt__(self,other):
        if isinstance(other, labfloat):
            return self.mean - self.uncertainty > other.mean + other.uncertainty
        if isinstance(other, Number):
            return self.mean - self.uncertainty > other

    def __le__(self,other):
        if isinstance(other, labfloat):
            return self.mean + self.uncertainty <= other.mean + other.uncertainty
        if isinstance(other, Number):
            return self.mean + self.uncertainty <= other

    def __ge__(self,other):
        if isinstance(other, labfloat):
            return self.mean - self.uncertainty >= other.mean - other.uncertainty
        if isinstance(other, Number):
            return self.mean - self.uncertainty >= other

    def __add__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self.mean + other.mean, sqrt(self.uncertainty ** 2 + other.uncertainty ** 2))
        if isinstance(other, Number):
            return labfloat(self.mean + other, self.uncertainty)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self.mean - other.mean, sqrt(self.uncertainty ** 2 + other.uncertainty ** 2))
        if isinstance(other, Number):
            return labfloat(self.mean - other, self.uncertainty)

    def __rsub__(self, other):
        if isinstance(other, labfloat):
            return labfloat(other.mean - self.mean, sqrt(other.uncertainty ** 2 + self.uncertainty ** 2))
        if isinstance(other, Number):
            return labfloat(other - self.mean, self.uncertainty)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self.mean * other.mean, sqrt((other.mean * self.uncertainty) ** 2 + (self.mean * other.uncertainty) ** 2))
        if isinstance(other, Number):
            return labfloat(self.mean * other, abs(other * self.uncertainty))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self.mean / other.mean, sqrt((self.uncertainty / other.mean) ** 2 + (self.mean * other.uncertainty / (other.mean ** 2)) ** 2 ))
        if isinstance(other, Number):
            return labfloat(self.mean / other, abs(self.uncertainty / other))

    def __truediv__(self, other):
        return self.__div__(other)

    def __idiv__(self, other):
        return self.__div__(other)

    def __itruediv__(self, other):
        return self.__div__(other)

    def __rdiv__(self, other):
        if isinstance(other, labfloat):
            return labfloat(other.mean / self.mean, sqrt((other.uncertainty / self.mean) ** 2 + (other.mean * self.uncertainty / (self.mean ** 2)) ** 2 ))
        if isinstance(other, Number):
            return labfloat(other / self.mean, abs(other * self.uncertainty / self.mean ** 2))

    def __rtruediv__(self, other):
        return self.__rdiv__(other)

    def __pow__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self.mean ** other.mean, sqrt((other.mean * self.mean ** (other.mean - 1) * self.uncertainty) ** 2 + (self.mean ** other.mean * log(abs(self.mean)) * other.uncertainty) ** 2))
        if isinstance(other, Number):
            return labfloat(self.mean ** other, abs(other * self.mean ** (other - 1) * self.uncertainty))

    def __rpow__(self, other):
        if isinstance(other, labfloat):
            return labfloat(other.mean ** self.mean, sqrt((self.mean * other.mean ** (self.mean - 1) * other.uncertainty) ** 2 + (other.mean ** self.mean * log(abs(other.mean)) * self.uncertainty) ** 2))
        if isinstance(other, Number):
            return labfloat(other ** self.mean, abs(other ** self.mean * log(abs(other)) * self.uncertainty))

    def __ipow__(self, other):
        return self.__pow__(other)

    def __int__(self):
        return int(self.mean)

    def __float__(self):
        return float(self.mean)

    def __complex__(self):
        return complex(self.mean)

    def __oct__(self):
        return oct(self.mean)

    def __hex__(self):
        return hex(self.mean)