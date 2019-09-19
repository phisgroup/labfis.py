from math import floor, ceil, trunc, log, log10
from numbers import Number

class labfloat:
    errsupport = "Essa operação não é suportado nesta classe, apenas as operações mencionadas na apostila de Laboratório de Física 2 do IFSC."

    def __init__(self, mean = 0.0, uncertainty = 0.0):
        self.mean = float(mean)
        self.uncertainty = float(abs(uncertainty))

    def __str__(self):
        if self.uncertainty == 0:
            return("{:g}".format(self.mean))
        else:
            su = str(self.uncertainty)
            i = su.find(".")
            if i == -1:
                r = - len(su) + 1
                m = round(self.mean, r)
                u = round(self.uncertainty, r)
                return("({:g} ± {:g})".format(m, u))
            else:
                r = -i
                r += 1
                for digit in su:
                    if digit == "0":
                        r += 1
                    elif digit != ".":
                        m = round(self.mean, r)
                        u = round(self.uncertainty, r)
                        return("({:g} ± {:g})".format(m, u))

        m = round(self.mean, r)
        u = round(self.uncertainty, r)
        return("({:g} ± {:g})".format(m, u))

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
            return abs(self.mean - other.mean) < 2 * (self.uncertainty - other.uncertainty)
        if isinstance(other, Number):
            return abs(self.mean - other) < 2 * self.uncertainty

    def __ne__(self, other):
        if isinstance(other, labfloat):
            return abs(self.mean - other.mean) > 3 * (self.uncertainty - other.uncertainty)
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
            return labfloat(self.mean + other.mean, self.uncertainty + other.uncertainty)
        if isinstance(other, Number):
            return labfloat(self.mean + other, self.uncertainty)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self.mean - other.mean, self.uncertainty + other.uncertainty)
        if isinstance(other, Number):
            return labfloat(self.mean - other, self.uncertainty)

    def __rsub__(self, other):
        if isinstance(other, labfloat):
            pass
        if isinstance(other, Number):
            return labfloat(other - self.mean, self.uncertainty)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self.mean * other.mean, self.mean * other.uncertainty + other.mean * self.uncertainty)
        if isinstance(other, Number):
            return labfloat(self.mean * other, other * self.uncertainty)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self.mean / other.mean, (self.mean * other.uncertainty + other.mean * self.uncertainty)/other.mean**2)
        if isinstance(other, Number):
            return labfloat(self.mean / other, self.uncertainty / other)

    def __truediv__(self, other):
        return self.__div__(other)

    def __idiv__(self, other):
        return self.__div__(other)

    def __itruediv__(self, other):
        return self.__div__(other)

    def __rdiv__(self, other):
        if isinstance(other, labfloat):
            return labfloat(other.mean / self.mean, (other.mean * self.uncertainty + self.mean * other.uncertainty)/self.mean**2)
        if isinstance(other, Number):
            return labfloat(other / self.mean, other * self.uncertainty / self.mean ** 2)

    def __rtruediv__(self, other):
        return self.__rdiv__(other)

    def __pow__(self, other):
        if isinstance(other, labfloat):
            raise Exception(self.errsupport)
        if isinstance(other, Number):
            return labfloat(self.mean ** other, other * self.mean ** (other-1) * self.uncertainty)

    def __rpow__(self, other):
        if isinstance(other, labfloat):
            raise Exception(self.errsupport)
        if isinstance(other, (float, int, hex, oct, complex)):
            return labfloat(other ** self.mean, other ** self.mean * log(other) * self.uncertainty)

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
