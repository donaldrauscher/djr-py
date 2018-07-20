from itertools import chain, combinations, combinations_with_replacement

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted, FLOAT_DTYPES, column_or_1d

import numpy as np

from scipy import sparse


# proportion of values in column not equal 0
def nonzero(X):
    freq = (X != 0).mean(axis=0)
    if sparse.isspmatrix(X):
        freq = freq.getA1()
    return freq


# version of PolynomialFeatures that accepts sparse matrices
class PolynomialFeatures(BaseEstimator, TransformerMixin):

    def __init__(self, degree=2, interaction_only=False, min_nz=0):
        self.degree = degree
        self.interaction_only = interaction_only
        self.min_nz = min_nz
        self._n_input_features = None
        self._combs = None

    @staticmethod
    def _make_combinations(features, degree, interaction_only):
        comb = (combinations if interaction_only else combinations_with_replacement)
        try:
            return chain.from_iterable(comb(features, i) for i in degree)
        except TypeError:
            return comb(features, degree)


    def fit(self, X, y=None):
        _, self._n_input_features = check_array(X, accept_sparse=True).shape

        features = np.where(nonzero(X) > self.min_nz)[0]
        combs = self._make_combinations(features, self.degree, self.interaction_only)
        combs = np.array([c for c in combs])

        mask = nonzero(self._transform(X, combs)) >= self.min_nz
        self._combs = combs[mask]
        return self

    @staticmethod
    def _transform(X, combs):

        X = check_array(X, dtype=FLOAT_DTYPES, accept_sparse='csc')
        n_samples = X.shape[0]

        if sparse.isspmatrix(X):
            columns = []
            for comb in combs:
                out_col = 1
                for col_idx in comb:
                    out_col = X[:, col_idx].multiply(out_col)
                columns.append(out_col)
            XP = sparse.hstack(columns, dtype=X.dtype)
        else:
            n_output_features = sum(1 for _ in combs)
            XP = np.empty((n_samples, n_output_features), dtype=X.dtype)
            for i, comb in enumerate(combs):
                XP[:, i] = X[:, comb].prod(1)

        return XP

    def transform(self, X):
        check_is_fitted(self, ['_n_input_features', '_combs'])

        n_features = X.shape[1]
        if n_features != self._n_input_features:
            raise ValueError("X shape does not match training shape")

        return self._transform(X, self._combs)


# builds interaction between a single column and an array of features
class InteractionTerm(BaseEstimator, TransformerMixin):

    def __init__(self, features, interaction):
        self.features = features
        self.interaction = interaction

    def get_feature_names(self):
        if not hasattr(self.features, 'get_feature_names'):
            raise AttributeError("`features` transformer  does not provide `get_feature_names`.")
        return self.features.get_feature_names()

    def fit(self, X, y=None):
        self.features = self.features.fit(X, y)
        self.interaction = self.interaction.fit(X, y)
        return self

    def transform(self, X):
        Xt = self.features.transform(X)
        ia = column_or_1d(self.interaction.transform(X)).reshape(-1, 1)

        if sparse.isspmatrix(Xt):
            Xt = Xt.multiply(ia)
        else:
            Xt *= ia

        return Xt
