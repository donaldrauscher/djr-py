import math
import numpy as np
from scipy import sparse
from sklearn.base import BaseEstimator, TransformerMixin

from .base import OneDimensionalTransformer
from .util import element_wise


# returns 0 if x < 0
def safe_log(x):
    return math.log1p(np.clip(x, 0, np.inf))


# transforms lognormal variable to normal
class LogNormalTransformer1D(OneDimensionalTransformer):

    def __init__(self):
        self.mu = None
        self.sig = None

    def _fit(self, X, y=None):
        X_log = np.array([safe_log(x) for x in X])
        self.mu = np.mean(X_log)
        self.sig = np.std(X_log)
        return self

    def _transform(self, X):
        return np.array([(safe_log(x) - self.mu)/self.sig for x in X])


# transforms lognormal variable to normal
class LogNormalTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.mu = None
        self.sig = None

    @staticmethod
    def log(x, copy=True):
        return element_wise(x.copy() if copy else x, safe_log)

    def fit(self, X, y=None):
        X_log = self.log(X)
        if sparse.isspmatrix(X):
            X_log2 = X_log.copy().multiply(X_log)
            self.mu = X_log.mean(axis=0).getA1()
            self.sig = np.sqrt(X_log2.mean(axis=0).getA1() - self.mu**2)
        else:
            self.mu = X_log.mean(axis=0)
            self.sig = X_log.std(axis=0)
        return self

    def transform(self, X):
        nrow = X.shape[0]
        mu = np.tile(self.mu, nrow).reshape(nrow, -1)
        sig = np.tile(self.sig, nrow).reshape(nrow, -1)
        return (self.log(X) - mu)/sig
