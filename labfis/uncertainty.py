import logging
from math import (floor, ceil, trunc, log, sqrt,
                  cos, sin, tan, asin, acos, atan)
from numbers import Number
from decimal import Decimal, getcontext, setcontext, Context, ROUND_HALF_UP

logger = logging.getLogger(__name__)

try:
    import numpy
except ImportError:
    numpy = None


class Infix:
    """definition of an Infix type operator class
    also works in jython,
    calling sequence for the infix is either:
    x |infix| y
    or:
    x <<infix>> y"""

    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return self.lbind(self.function, other)

    def __or__(self, other):
        return self.rbind(self.function, other)

    def __rlshift__(self, other):
        return self.lbind(self.function, other)

    def __rshift__(self, other):
        return self.rbind(self.function, other)

    class rbind:
        def __init__(self, function, binded):
            self.function = function
            self.binded = binded

        def __ror__(self, other):
            return self.function(other, self.binded)

        def __rlshift__(self, other):
            return self.function(other, self.binded)

        def __call__(self, other):
            return self.function(other, self.binded)

    class lbind:
        def __init__(self, function, binded):
            self.function = function
            self.binded = binded

        def __or__(self, other):
            return self.function(self.binded, other)

        def __rshift__(self, other):
            return self.function(self.binded, other)

        def __call__(self, other):
            return self.function(self.binded, other)


class LabFloatError(Exception):
    def __init__(self, *args):
        if args:
            if args[0] == 0:
                self.message = "This operation is not supported."
            elif args[0] == 1:
                self.message = "Too many arguments, expected '(val,err)' or '([val1,val2,...],[err1,err2,...],...)' , got: '{0}'".format(
                    args[1])
            elif args[0] == 2:
                self.message = "Mean list and Uncertainty list must have the same size, expected: '[val1,val2,...,valn],[err1,err2,...,errn]' , got: '{0}'".format(
                    args[1:])
            elif args[0] == 3:
                self.message = "Uncertanty or mean list missing, expected: '[*vals1],[*errs1],[*vals2],[*errs2],...,[*valsn],[*errsn]' , got: '{0}'".format(
                    args[1])
            elif args[0] == 4:
                self.message = "Too many arguments, expected: '(precision)' or '(mean precision,err precision)' , got: '{0}'".format(
                    args[1])
            elif isinstance(args[0], str):
                self.message = args[0] % args[1:]
            else:
                self.message = None
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        return 'A generic LabFloatError has been raised'


class labfloat:
    context = Context(rounding=ROUND_HALF_UP)

    def __new__(cls, *args, **kwargs):
        listlabfloat = kwargs.get('list', [])
        if args:
            if numpy:
                if isinstance(args[0], (list, numpy.ndarray)):
                    listlabfloat = args
            else:
                if isinstance(args[0], list):
                    listlabfloat = args
        if listlabfloat != []:
            if len(listlabfloat) % 2 != 0:
                raise LabFloatError(3, listlabfloat)
            return cls.list(listlabfloat)

        return object.__new__(cls)

    def __init__(self, *args, **kwargs):
        mean = kwargs.get('mean', 0.0)
        uncertainty = kwargs.get('uncertainty', 0.0)

        if args:
            if len(args) == 1:
                mean = args[0]
            elif len(args) == 2:
                mean = args[0]
                uncertainty = args[1]
            elif len(args) > 2:
                raise LabFloatError(1, args)

        self._mean = mean
        self._uncertainty = abs(uncertainty)

    @classmethod
    def list(cls, listargs):
        listlabfloat = []
        for j in range(0, len(listargs), 2):
            if len(listargs[j]) == len(listargs[j + 1]):
                colum = []
                for k in range(len(listargs[j])):
                    colum += [cls(listargs[j][k], listargs[j + 1][k])]
                listlabfloat += [colum]
            else:
                raise LabFloatError(2, listargs[j], listargs[j + 1])
        if len(listlabfloat) == 1:
            listlabfloat = listlabfloat[0]
        return listlabfloat

    def __round__(self, p=0):
        current_contex = getcontext()
        setcontext(self.context)
        
        u = Decimal(self._uncertainty)
        m = Decimal(self._mean)

        p += -u.adjusted()*(not p)

        u = round(u, p)
        m = round(m, p)
        
        setcontext(current_contex)

        return m, u

    def split(self):
        m, u = self.__round__()
        return ["{:g}".format(m), "{:g}".format(u)]

    def tex(self, *args, **kwargs):
        precision = kwargs.get('precision')
        if args:
            if len(args) == 2:
                precision = args
            elif len(args) > 2:
                raise LabFloatError(4, args)
            else:
                precision = [args[0], args[0]]

        if self._uncertainty == 0:
            if precision:
                precision[0] = str(precision[0])
                m = eval("'{:." + precision[0] + "e}'.format(self._mean)")
            else:
                m = self.split()[0]
            m = m.split("e")
            if len(m) > 1:
                m = m[0] + r"\cdot 10^{" + m[1] + "}"
            else:
                m = m[0]
            return "{0}".format(m)

        if precision:
            precision = (str(precision[0]), str(precision[1]))
            m, u = self.__round__()
            m = eval("'{:." + precision[0] + "e}'.format(m)")
            u = eval("'{:." + precision[1] + "e}'.format(u)")
        else:
            m, u = self.split()
        m = m.split("e")
        u = u.split("e")
        if len(m) > 1:
            m = m[0] + r"\cdot 10^{" + m[1] + "}"
        else:
            m = m[0]
        if len(u) > 1:
            u = u[0] + r"\cdot 10^{" + u[1] + "}"
        else:
            u = u[0]
        return r"({0}\, \pm \,{1})".format(m, u)

    def __str__(self):
        return "({0} ± {1})".format(*self.split())

    def __repr__(self):
        return self.__str__()

    @property
    def mean(self):
        return self._mean

    @property
    def uncertainty(self):
        return self._uncertainty

    def __getitem__(self, idx):
        vals = (self.uncertainty, self.mean)
        return vals[idx]

    def __pos__(self):
        return self

    def __neg__(self):
        return labfloat(-self._mean, self._uncertainty)

    def __abs__(self):
        return labfloat(abs(self._mean), self._uncertainty)

    def __floor__(self):
        return labfloat(floor(self._mean), floor(self._uncertainty))

    def __ceil__(self):
        return labfloat(ceil(self._mean), ceil(self._uncertainty))

    def __trunc__(self):
        return labfloat(trunc(self._mean), trunc(self._uncertainty))

    def __eq__(self, other):
        if isinstance(other, labfloat):
            return abs(self._mean - other.mean) < 2 * (self._uncertainty + other.uncertainty)
        if isinstance(other, Number):
            return abs(self._mean - other) < 2 * self._uncertainty

    def __ne__(self, other):
        if isinstance(other, labfloat):
            return abs(self._mean - other.mean) > 3 * (self._uncertainty + other.uncertainty)
        if isinstance(other, Number):
            return abs(self._mean - other) > 3 * self._uncertainty

    def __lt__(self, other):
        if isinstance(other, labfloat):
            return self._mean + self._uncertainty < other.mean - other.uncertainty
        if isinstance(other, Number):
            return self._mean + self._uncertainty < other

    def __gt__(self, other):
        if isinstance(other, labfloat):
            return self._mean - self._uncertainty > other.mean + other.uncertainty
        if isinstance(other, Number):
            return self._mean - self._uncertainty > other

    def __le__(self, other):
        if isinstance(other, labfloat):
            return self._mean + self._uncertainty <= other.mean + other.uncertainty
        if isinstance(other, Number):
            return self._mean + self._uncertainty <= other

    def __ge__(self, other):
        if isinstance(other, labfloat):
            return self._mean - self._uncertainty >= other.mean - other.uncertainty
        if isinstance(other, Number):
            return self._mean - self._uncertainty >= other

    def __add__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self._mean + other.mean, sqrt(self._uncertainty ** 2 + other.uncertainty ** 2))
        if isinstance(other, Number):
            return labfloat(self._mean + other, self._uncertainty)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self._mean - other.mean, sqrt(self._uncertainty ** 2 + other.uncertainty ** 2))
        if isinstance(other, Number):
            return labfloat(self._mean - other, self._uncertainty)

    def __rsub__(self, other):
        if isinstance(other, labfloat):
            return labfloat(other.mean - self._mean, sqrt(other.uncertainty ** 2 + self._uncertainty ** 2))
        if isinstance(other, Number):
            return labfloat(other - self._mean, self._uncertainty)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self._mean * other.mean, sqrt((other.mean * self._uncertainty) ** 2 + (self._mean * other.uncertainty) ** 2))
        if isinstance(other, Number):
            return labfloat(self._mean * other, abs(other * self._uncertainty))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self._mean / other.mean, sqrt((self._uncertainty / other.mean) ** 2 + (self._mean * other.uncertainty / (other.mean ** 2)) ** 2))
        if isinstance(other, Number):
            return labfloat(self._mean / other, abs(self._uncertainty / other))

    def __truediv__(self, other):
        return self.__div__(other)

    def __idiv__(self, other):
        return self.__div__(other)

    def __itruediv__(self, other):
        return self.__div__(other)

    def __rdiv__(self, other):
        if isinstance(other, labfloat):
            return labfloat(other.mean / self._mean, sqrt((other.uncertainty / self._mean) ** 2 + (other.mean * self._uncertainty / (self._mean ** 2)) ** 2))
        if isinstance(other, Number):
            return labfloat(other / self._mean, abs(other * self._uncertainty / self._mean ** 2))

    def __rtruediv__(self, other):
        return self.__rdiv__(other)

    def __pow__(self, other):
        if isinstance(other, labfloat):
            return labfloat(self._mean ** other.mean, sqrt((other.mean * self._mean ** (other.mean - 1) * self._uncertainty) ** 2 + (self._mean ** other.mean * log(abs(self._mean)) * other.uncertainty) ** 2))
        if isinstance(other, Number):
            return labfloat(self._mean ** other, abs(other * self._mean ** (other - 1) * self._uncertainty))

    def __rpow__(self, other):
        if isinstance(other, labfloat):
            return labfloat(other.mean ** self._mean, sqrt((self._mean * other.mean ** (self._mean - 1) * other.uncertainty) ** 2 + (other.mean ** self._mean * log(abs(other.mean)) * self._uncertainty) ** 2))
        if isinstance(other, Number):
            return labfloat(other ** self._mean, abs(other ** self._mean * log(abs(other)) * self._uncertainty))

    def __ipow__(self, other):
        return self.__pow__(other)

    def sqrt(self):
        return self.__pow__(0.5)

    def cos(self):
        return labfloat(cos(self._mean), abs(-(sin(self._mean)) * self._uncertainty))

    def sin(self):
        return labfloat(sin(self._mean), abs(cos(self._mean) * self._uncertainty))

    def tan(self):
        return labfloat(tan(self._mean), sqrt((cos(self._mean) ** -4) * self._uncertainty ** 2))

    def arcsin(self):
        return labfloat(asin(self._mean), self._uncertainty / sqrt(1 - self._mean ** 2))

    def arccos(self):
        return labfloat(acos(self._mean), abs(-self._uncertainty / sqrt(1 - self._mean ** 2)))

    def arctan(self):
        return labfloat(atan(self._mean), self._uncertainty / (1 + self._mean ** 2))

    def __int__(self):
        return int(self._mean)

    def __float__(self):
        return float(self._mean)

    def __complex__(self):
        return complex(self._mean)

    def __oct__(self):
        return oct(self._mean)

    def __hex__(self):
        return hex(self._mean)
