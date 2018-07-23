import pytest

import numpy as np
from scipy import sparse

from ..util import element_wise, safe_divide, first_non_null, flatten_dict, remove_prefix


ones = np.ones(9).reshape(3, 3)
twos = np.repeat(2, 9).reshape(3, 3)

ones_sparse = sparse.csr_matrix(np.identity(3))
twos_sparse = sparse.csr_matrix(np.identity(3)*2)


def test_element_wise():
    assert np.array_equal(element_wise(ones, lambda x: x + 1), twos)


def test_element_wise_sparse():
    assert np.array_equal(element_wise(ones_sparse, lambda x: x*2).toarray(),
                          twos_sparse.toarray())


def test_zero_divide():
    assert safe_divide(1, 0, -1) == -1


def test_first_non_null():
    assert first_non_null(np.array([np.nan, 2.0])) == 2.0
    with pytest.raises(ValueError):
        first_non_null(ones)


def test_dict():
    qc1 = {'a': 1, 'x': {'b': 2, 'c': 3}}
    qc2 = {'a': 1, 'x__b': 2, 'x__c': 3}
    qc3 = {'a': 1, 'b': 2, 'c': 3}
    assert flatten_dict(qc1) == qc2
    assert remove_prefix(flatten_dict(qc1)) == qc3
