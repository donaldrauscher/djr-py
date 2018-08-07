import numpy as np
from sklearn.preprocessing import FunctionTransformer
from ..preprocessing import FeatureUnionIID


transformers = [('fe{}'.format(i), FunctionTransformer(func=lambda x, a: x + a)) for i in range(3)]
iid = FeatureUnionIID(transformer_list=transformers)
iid.set_params(**{'kw_args': {'a': 1}})

x = np.ones(3).reshape(-1, 1)
twos = np.repeat(2, 9).reshape(3, 3)


def test_iid_one():
    assert np.array_equal(iid.fit_transform(x), twos)
