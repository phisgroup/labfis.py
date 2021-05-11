from random import uniform
from labfis import u, labfloat 

def test_infix():
    for _ in range(200):
        x, e = uniform(-2e50,2e50), uniform(-2e50,2e50) 
        assert labfloat(x, e) == x |u| e == x <<u>> e

class TestInitialization():
    def test_empty_eq_zero(self):
        assert labfloat() == labfloat(0, 0)

    def test_int_eq_float(self):
        assert labfloat(10, 2) == labfloat(10., 2.) 

    def test_attrs(self):
        x = labfloat(10, 1)
        assert x.mean == 10 and x.uncertainty == 1
