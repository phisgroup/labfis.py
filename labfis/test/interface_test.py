from random import uniform
from labfis import u, labfloat


def test_infix():
    for _ in range(200):
        x, e = uniform(-2e50, 2e50), uniform(-2e50, 2e50)
        assert labfloat(x, e) == x | u | e == x << u >> e


def test_attrs():
    x = labfloat(10, 1)
    assert x.mean == 10 and x.uncertainty == 1
