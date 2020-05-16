import pytest
import numpy
from math import sqrt
import labfis

dx = 1e-13


def labfloat_iterative(vardic, exp):
    resulterror = 0

    for var in vardic.keys():
        exec(var + "=" + "{0:.16f}".format(vardic[var][0]))

    for var in vardic.keys():
        var_value = vardic[var][0]
        var_error = vardic[var][1]

        exec(var + "=" + "{0:.16f}".format(var_value) +
             "+" + "{0:.16f}".format(dx))
        dph = eval(exp)

        exec(var + "=" + "{0:.16f}".format(var_value))
        dpn = eval(exp)

        derivative = (dph - dpn)/dx
        resulterror += (derivative * var_error) ** 2
    return sqrt(resulterror)


def labfloat_calc(vardic, exp):
    for var in vardic.keys():
        exec(var + "=" +
             "labfis.labfloat({0:.16f},{1:.16f})".format(*vardic[var]))
    result = eval(exp)
    return result.uncertainty


rng = numpy.random.default_rng()

expresions = [
    "a*b*c",
    "a*b/c",
    "(a**b)*c",
    "2/b*(a/c)",
    "a+b+c",
    "a-b+c",
    "c**b/a",
    "(c**0.5+b**1.3)*"+str(numpy.e)+"**a"
]

vals = {
    "a": (rng.random(), rng.random()),
    "b": (rng.random(), rng.random()),
    "c": (rng.random(), rng.random())
}


def test_labfloat_expressions():
    for exp in expresions:
        result1 = labfloat_iterative(vals, exp)
        result2 = labfloat_calc(vals, exp)

        print(result1, result2)

        assert round(result2) == round(result1)
