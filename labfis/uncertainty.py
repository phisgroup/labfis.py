from __future__ import annotations
import logging
from collections.abc import Iterable
from typing import Union, Tuple, List
from math import floor, ceil, trunc, log, cos, sin, tan, asin, acos, atan
from numbers import Number
from decimal import Decimal, getcontext, setcontext, Context, ROUND_HALF_UP

logger = logging.getLogger(__name__)


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
                    args[1]
                )
            elif args[0] == 2:
                self.message = "Mean list and Uncertainty list must have the same size, expected: '[val1,val2,...,valn],[err1,err2,...,errn]' , got: '{0}'".format(
                    args[1:]
                )
            elif args[0] == 3:
                self.message = "Uncertanty or mean list missing, expected: '[*vals1],[*errs1],[*vals2],[*errs2],...,[*valsn],[*errsn]' , got: '{0}'".format(
                    args[1]
                )
            elif args[0] == 4:
                self.message = "Too many arguments, expected: '(precision)' or '(mean precision,err precision)' , got: '{0}'".format(
                    args[1]
                )
            elif isinstance(args[0], str):
                self.message = args[0] % args[1:]
            else:
                self.message = None
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        return "A generic LabFloatError has been raised"


class labfloat:
    """Represents a gaussian distribution.

    A labfloat object stores an gaussian's distribuition mean and standard deviation, in
    witch can be used to represent a experimental physical measure. Therefore, all
    arithmetics calculations done with this object will properlly propagate it's error
    analytically in accordance with the gaussian propagation formula. Furthermore, the
    comparison methods are also using the statistical relation testing equations.

    If one or more list is passed as an argument, it will call labfloat.list()
    to convert the nested list and return the nested list of labfloats. Or else,
    it will create an single instance of labfloat.

    Raises:
        LabFloatError: Labfloat Generic error due to missused interface.

    """

    context = Context(rounding=ROUND_HALF_UP)
    """Context: Set ROUND_HALF_UP for the decimals used in __round__ method."""

    def __new__(cls, *args, **kwargs) -> Union[object, Iterable]:
        """Create an instance of labfloat or a nested list of labfloat.

        If one or more list is passed as an argument, it will call labfloat.list()
        to convert the nested list and return the nested list of labfloats. Or else,
        it will create an single instance of labfloat.

        Raises:
            LabFloatError: Missing errors or means list to convert nested list.

        Returns:
            Union[object, Iterable]: Nested list of labfloat or a new labfloat object.

        Examples:
            >>> labfloat(1,3)
            >>> labfloat([1,2,3,4],[1,1,1,1])
            >>> labfloat([15,16,17,18],[10,10,10,10],[16,17,18,19],[10,10,10,10])

        """
        listlabfloat = kwargs.get("list", [])
        if args:
            if isinstance(args[0], Iterable):
                listlabfloat = args
        if listlabfloat != []:
            if len(listlabfloat) % 2 != 0:
                raise LabFloatError(3, listlabfloat)
            return cls.list(listlabfloat)

        return object.__new__(cls)

    def __init__(self, *args, **kwargs):
        """Create an instance of labfloat or a nested list of labfloat.

        If one or more list is passed as an argument, it will call labfloat.list()
        to convert the nested list and return the nested list of labfloats. Or else,
        it will create an single instance of labfloat.

        Raises:
            LabFloatError: Missing errors or means list to convert nested list.
            LabFloatError: Too many arguments.

        Returns:
            Union[object, Iterable]: Nested list of labfloat or a new labfloat object.

        Examples:
            >>> labfloat(1,3)
            >>> labfloat([1,2,3,4],[1,1,1,1])
            >>> labfloat([15,16,17,18],[10,10,10,10],[16,17,18,19],[10,10,10,10])

        """
        # NOTE: docstring the same as __new__ method due to editor only showing __init__ docstring.
        mean = kwargs.get("mean", 0.0)
        uncertainty = kwargs.get("uncertainty", 0.0)

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
    def list(cls, listargs: Iterable) -> Iterable:
        """Convert nested list of means and errors to nested list of labfloat.

        Args:
            listargs (Iterable): Nested list of means and list of erros.

        Raises:
            LabFloatError: Means list and erros list does not have the same length.

        Returns:
            Iterable: Nested list of labfloats.

        """
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

    def __round__(self, p: int = 0) -> labfloat:
        """Round labfloat's mean and uncertainty at p decimal places.

        When no arguments are passed or p=0, the mean and uncertainty will round at the
        uncertainty most significant figure to nearest with ties going away from zero
        (Round half away from zero) using Python's ROUND_HALF_UP. If a value is passe to
        p it will round at p decimal places, and if p is greater than the error's most
        significant figure decimal place, the error will be one at the mean's least
        significant figure decimal place.

        Args:
            p (int, optional): The number of decimals to use when rounding. Defaults to 0.

        Returns:
            labfloat: New labfloat with the rounded mean and error.

        """
        current_contex = getcontext()
        setcontext(self.context)

        u = Decimal(str(self._uncertainty))
        m = Decimal(str(self._mean))

        r = p - u.adjusted() * (not p)

        u = round(u, r)

        r = p - u.adjusted() * (not p)

        u += Decimal("1e{}".format(-r)) * (not u)

        m = round(m, r)

        setcontext(current_contex)

        return labfloat(type(self._mean)(m), type(self._uncertainty)(u))

    def split(self) -> List[str]:
        """Split the string representation of labfloat.

        The split is done in the ± keyword.

        Returns:
            List[str]: rounded labfloat's mean and error in str format.

        """
        m, u = self.__round__()
        return ["{:g}".format(m), "{:g}".format(u)]

    def tex(
        self, precision: Union[Tuple[float], float] = None, round_p: int = 0
    ) -> str:
        """Convert labfloat to string representation in LaTex format.

        The arguments precision and round_p are used to configure the display precision and round
        decimal places. The precision is a float in "0.0" format.

        Args:
            precision (Union[Tuple[float], float], optional): A tuple containing the mean's and error's precision or only one string for both precisions. If no value are passed the default precision. Defaults to None.
            round_p (int, optional): Number of decimals to use when rounding. Defaults to 0.

        Raises:
            LabFloatError: Error in parsing arguments, where the number of precision tuple is greater than 2.

        Returns:
            str: labfloat's strig representation in LaTex format.

        """
        if isinstance(precision, tuple):
            if len(precision) > 2:
                raise LabFloatError(4, precision)
            precision = (float(precision[0]), float(precision[1]))
        elif precision:
            precision = (float(precision), float(precision))

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
            m, u = self.__round__(round_p)
            precision = (str(precision[0]), str(precision[1]))
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

    def __str__(self) -> str:
        """Convert the labfloat to it's string representation.

        For conventional displaying pourposes the lablofat will be rouded using the
        default method.

        Returns:
            str: gaussian distribuiton mean and error string representation.

        """
        return "({0} ± {1})".format(*self.split())

    def __repr__(self) -> str:
        """Represent labfloat as a string object.

        Returns:
            str: labfloat's string convertion.

        """
        return self.__str__()

    @property
    def mean(self) -> object:
        """object: labfloat's mean."""
        return self._mean

    @property
    def uncertainty(self) -> object:
        """object: labfloat's error."""
        return self._uncertainty

    def __getitem__(self, idx: int) -> Tuple[object]:
        """Represent the labfloat as an tuple.

        This method indexes the labfloat's attributes mean and erro as an tuple object.
        Therefore, with this magic method labfloat can be used as an tuple.

        Args:
            idx (int): idex position of the labfis tuple representation

        Returns:
            Tuple[object]: A tuple with labfloat's mean and error.

        Example:
            >>> a, b = labfloat(1,3)
            >>> print(*labfloat(1,3))
            >>> for i in labfloat(1,3): print(i)

        """
        vals = (self.mean, self.uncertainty)
        return vals[idx]

    def __pos__(self) -> labfloat:
        return self

    def __neg__(self) -> labfloat:
        return labfloat(-self._mean, self._uncertainty)

    def __abs__(self) -> labfloat:
        return labfloat(abs(self._mean), self._uncertainty)

    def __floor__(self) -> labfloat:
        return labfloat(floor(self._mean), floor(self._uncertainty))

    def __ceil__(self) -> labfloat:
        return labfloat(ceil(self._mean), ceil(self._uncertainty))

    def __trunc__(self) -> labfloat:
        return labfloat(trunc(self._mean), trunc(self._uncertainty))

    def __eq__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return abs(self._mean - other.mean) < 2 * (
                self._uncertainty + other.uncertainty
            )
        if isinstance(other, Number):
            return abs(self._mean - other) < 2 * self._uncertainty

        return None

    def __ne__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return abs(self._mean - other.mean) > 3 * (
                self._uncertainty + other.uncertainty
            )
        if isinstance(other, Number):
            return abs(self._mean - other) > 3 * self._uncertainty

        return None

    def __lt__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return self._mean + self._uncertainty < other.mean - other.uncertainty
        if isinstance(other, Number):
            return self._mean + self._uncertainty < other

        return None

    def __gt__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return self._mean - self._uncertainty > other.mean + other.uncertainty
        if isinstance(other, Number):
            return self._mean - self._uncertainty > other

        return None

    def __le__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return self._mean + self._uncertainty <= other.mean + other.uncertainty
        if isinstance(other, Number):
            return self._mean + self._uncertainty <= other

        return None

    def __ge__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return self._mean - self._uncertainty >= other.mean - other.uncertainty
        if isinstance(other, Number):
            return self._mean - self._uncertainty >= other

        return None

    def __add__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return labfloat(
                self._mean + other.mean,
                (self._uncertainty ** 2 + other.uncertainty ** 2) ** 0.5,
            )
        if isinstance(other, Number):
            return labfloat(self._mean + other, self._uncertainty)

        return None

    def __radd__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__add__(other)

    def __iadd__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__add__(other)

    def __sub__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return labfloat(
                self._mean - other.mean,
                (self._uncertainty ** 2 + other.uncertainty ** 2) ** 0.5,
            )
        if isinstance(other, Number):
            return labfloat(self._mean - other, self._uncertainty)

        return None

    def __rsub__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return labfloat(
                other.mean - self._mean,
                (other.uncertainty ** 2 + self._uncertainty ** 2) ** 0.5,
            )
        if isinstance(other, Number):
            return labfloat(other - self._mean, self._uncertainty)

        return None

    def __isub__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__sub__(other)

    def __mul__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return labfloat(
                self._mean * other.mean,
                (
                    (other.mean * self._uncertainty) ** 2
                    + (self._mean * other.uncertainty) ** 2
                )
                ** 0.5,
            )
        if isinstance(other, Number):
            return labfloat(self._mean * other, abs(other * self._uncertainty))

        return None

    def __rmul__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__mul__(other)

    def __imul__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__mul__(other)

    def __div__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return labfloat(
                self._mean / other.mean,
                (
                    (self._uncertainty / other.mean) ** 2
                    + (self._mean * other.uncertainty / (other.mean ** 2)) ** 2
                )
                ** 0.5,
            )
        if isinstance(other, Number):
            return labfloat(self._mean / other, abs(self._uncertainty / other))

        return None

    def __truediv__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__div__(other)

    def __idiv__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__div__(other)

    def __itruediv__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__div__(other)

    def __rdiv__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return labfloat(
                other.mean / self._mean,
                (
                    (other.uncertainty / self._mean) ** 2
                    + (other.mean * self._uncertainty / (self._mean ** 2)) ** 2
                )
                ** 0.5,
            )
        if isinstance(other, Number):
            return labfloat(
                other / self._mean, abs(other * self._uncertainty / self._mean ** 2)
            )

        return None

    def __rtruediv__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__rdiv__(other)

    def __pow__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return labfloat(
                self._mean ** other.mean,
                (
                    (other.mean * self._mean ** (other.mean - 1) * self._uncertainty)
                    ** 2
                    + (
                        self._mean ** other.mean
                        * log(abs(self._mean))
                        * other.uncertainty
                    )
                    ** 2
                )
                ** 0.5,
            )
        if isinstance(other, Number):
            return labfloat(
                self._mean ** other,
                abs(other * self._mean ** (other - 1) * self._uncertainty),
            )

        return None

    def __rpow__(self, other: Union[labfloat, Number]) -> labfloat:
        if isinstance(other, labfloat):
            return labfloat(
                other.mean ** self._mean,
                (
                    (self._mean * other.mean ** (self._mean - 1) * other.uncertainty)
                    ** 2
                    + (
                        other.mean ** self._mean
                        * log(abs(other.mean))
                        * self._uncertainty
                    )
                    ** 2
                )
                ** 0.5,
            )
        if isinstance(other, Number):
            return labfloat(
                other ** self._mean,
                abs(other ** self._mean * log(abs(other)) * self._uncertainty),
            )

        return None

    def __ipow__(self, other: Union[labfloat, Number]) -> labfloat:
        return self.__pow__(other)

    def sqrt(self) -> labfloat:
        return self.__pow__(0.5)

    def cos(self) -> labfloat:
        return labfloat(cos(self._mean), abs(-(sin(self._mean)) * self._uncertainty))

    def sin(self) -> labfloat:
        return labfloat(sin(self._mean), abs(cos(self._mean) * self._uncertainty))

    def tan(self) -> labfloat:
        return labfloat(
            tan(self._mean), ((cos(self._mean) ** -4) * self._uncertainty ** 2) ** 0.5
        )

    def arcsin(self) -> labfloat:
        return labfloat(asin(self._mean), self._uncertainty / (1 - self._mean ** 2))

    def arccos(self) -> labfloat:
        return labfloat(
            acos(self._mean), abs(-self._uncertainty / (1 - self._mean ** 2)) ** 0.5
        )

    def arctan(self) -> labfloat:
        return labfloat(atan(self._mean), self._uncertainty / (1 + self._mean ** 2))

    def __int__(self) -> int:
        return int(self._mean)

    def __float__(self) -> float:
        return float(self._mean)

    def __complex__(self) -> complex:
        return complex(self._mean)

    def __oct__(self) -> oct:
        return oct(self._mean)

    def __hex__(self) -> hex:
        return hex(self._mean)
