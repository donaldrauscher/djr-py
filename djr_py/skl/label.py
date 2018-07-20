import pandas as pd
import numpy as np

from sklearn.utils.validation import check_is_fitted

from .base import OneDimensionalTransformer


# labeler which handles missing labels
class LabelEncoder(OneDimensionalTransformer):

    def __init__(self, top_n=np.inf, min_support=30):
        self.top_n = top_n
        self.min_support = min_support
        self.classes_ = None
        self.has_other_ = False

    # include 'other' category if relevant
    @property
    def classes(self):
        classes = [str(c) for c in self.classes_.tolist()]
        return classes + ['other'] if self.has_other_ else classes

    def _fit(self, X, y=None):
        classes1 = pd.Series(X).value_counts()
        classes2 = classes1[classes1 >= self.min_support]
        if not np.isinf(self.top_n):
            classes2 = classes2.head(self.top_n)
        classes2 = np.sort(classes2.index)

        self.classes_ = classes2
        self.has_other_ = len(classes1) > len(classes2)

        return self

    def _transform(self, X):
        check_is_fitted(self, 'classes_')

        new_label = ~np.in1d(X, self.classes_)
        labels = np.searchsorted(self.classes_, X)
        labels[new_label] = len(self.classes_)

        return labels
