import numpy as np
from ..label import LabelEncoder


le = LabelEncoder(min_support=2)
x = np.concatenate([np.repeat([1, 2, 3], 2), [4, 5, 6]])
x2 = le.fit_transform(x).flatten()


def test_labeler_one():
    assert len(le.classes) == 4 and le.classes[-1] == 'other'


def test_labeler_two():
    assert len(np.unique(x2)) == 4