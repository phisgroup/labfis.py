from labfis import labfloat as lf
from itertools import combinations

def test_zeros():
    zeros = [lf(),lf(0),lf(0.),lf(0,0),
            lf(0.,0.),lf(0.,0),lf(0,0.),0,0.]
    for z1, z2 in combinations(zeros, 2):
        assert z1 == z2 

def test_indexing():
    assert lf(10,2)[:] == [10,2]

def TestUnary():
    def test_pos(self):
        x = lf(100,4)
        assert x == +x

    def test_neg():
        x = lf(243,2)
        y = lf(-243,2)
        assert x == -y

#TODO: test cases for other arithmetic operators
