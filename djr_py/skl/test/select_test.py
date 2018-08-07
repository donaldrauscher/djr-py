import numpy as np
from ..select import SelectDocFreq


n = 5
X = np.ones(n**2).reshape(n, n)
X[np.triu_indices(n, 1)] = 0
y = np.ones(n)
min_df = 1.0/n + 0.01
max_df = (n - 1.0)/n + 0.01


def test_select_doc_freq():
    sdf = SelectDocFreq(min_df=min_df, max_df=max_df)
    qc = sdf.fit_transform(X, y)
    assert qc.shape == (n, n - 2)
    assert qc.sum() == (n * (n + 1) / 2 - n - 1)
