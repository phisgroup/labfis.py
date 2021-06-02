from itertools import combinations
from labfis import labfloat


def test_zeros():
    zeros = [
        labfloat(),
        labfloat(0),
        labfloat(0.0),
        labfloat(0, 0),
        labfloat(0.0, 0.0),
        labfloat(0.0, 0),
        labfloat(0, 0.0),
    ]

    for z1, z2 in combinations(zeros, 2):
        print(z1, z2)
        assert list(z1) == list(z2)


def test_indexing():
    assert labfloat(10, 2)[:] == (10, 2)


def TestUnary():
    def test_pos():
        x = labfloat(100, 4)
        y = +x

        assert list(x) == list(y)

    def test_neg_mean():
        x = labfloat(243, 2)
        y = labfloat(-243, 2)
        y = -y

        assert list(x) == list(y)

    def test_neg_uncertainty():
        x = labfloat(243, 2)
        y = labfloat(243, -2)

        assert list(x) == list(y)


# TODO: test cases for other arithmetic operators
