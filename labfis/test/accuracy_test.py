import pytest
import numpy
import itertools
from math import sqrt
import labfis

dx = 1e-8


def labfloat_iterative(vardic, exp):
    resulterror = 0

    for var in vardic.keys():
        exec(var + "=" + "vardic[var][0]")

    for var in vardic.keys():
        var_value = vardic[var][0]
        var_error = vardic[var][1]

        exec(var + "=" + "var_value" + "+" + "dx")
        dph = eval(exp)

        exec(var + "=" + "var_value")
        dpn = eval(exp)

        derivative = (dph - dpn) / dx
        resulterror += (derivative ** 2) * (var_error ** 2)
    return sqrt(resulterror)


def labfloat_calc(vardic, exp):
    for var in vardic.keys():
        exec(var + "=" + "labfis.labfloat(vardic[var][0],vardic[var][1])")
    result = eval(exp)
    return result.uncertainty


rng = numpy.random.default_rng()

operations = ["*", "/", "+", "-", "**"]

vals = {
    "a": (rng.random(), rng.random()),
    "b": (rng.random(), rng.random()),
    "c": (rng.random(), rng.random()),
    "d": (rng.random(), rng.random()),
    "e": (rng.random(), rng.random()),
}


def test_labfloat_expressions():
    print(vals)
    var = list(vals.keys())
    opers = itertools.combinations_with_replacement(operations, len(var) - 1)
    for exp in opers:
        expression = ""
        for i in range(len(exp)):
            if i == len(exp) - 1:
                expression += var[i] + exp[i] + var[i + 1]
            else:
                expression += var[i] + exp[i]

        result1 = labfloat_iterative(vals, expression)
        result2 = labfloat_calc(vals, expression)

        error = abs(result2 - result1) / result2

        print(expression)
        print(type(result1), type(result2))
        print("numerical: {}".format(result1), "analitical: {}".format(result2))

        assert error < 1e-5
