import numpy as np

from sklearn.feature_selection.univariate_selection import _BaseFilter
from sklearn.utils.validation import check_is_fitted

import scipy


# proportion of values greater than 0
def doc_freq(X, y=None):
    freq = (X > 0).mean(axis=0)
    if scipy.sparse.isspmatrix(X):
        freq = freq.getA1()
    return freq


# provides just min/max document frequency from CountVectorizer
class SelectDocFreq(_BaseFilter):

    def __init__(self, max_df=1.0, min_df=0.01):
        super(SelectDocFreq, self).__init__(doc_freq)
        self.max_df = max_df
        self.min_df = min_df

    def _check_params(self, X, y):
        if not 0 <= self.min_df <= 1:
            raise ValueError("min_df should be >=0, <=1; got %r" % self.min_df)
        if not 0 <= self.max_df <= 1:
            raise ValueError("max_df should be >=0, <=1; got %r" % self.max_df)

    def _get_support_mask(self):
        check_is_fitted(self, 'scores_')
        scores = self.scores_
        mask = np.logical_and(scores >= self.min_df, scores <= self.max_df)
        return mask
