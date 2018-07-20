import abc

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline as BasePipeline
from sklearn.utils.validation import column_or_1d


# pipeline class with feature names function
class Pipeline(BasePipeline):
    def __init__(self, steps, fn):
        super(Pipeline, self).__init__(steps)
        self.fn = fn

    def get_feature_names(self):
        return self.fn(self.steps)


# transformer which works on a single dimension
class OneDimensionalTransformer(BaseEstimator, TransformerMixin):

    @abc.abstractmethod
    def _fit(self, X, y=None):
        pass

    @abc.abstractmethod
    def _transform(self, X):
        pass

    def fit(self, X, y=None):
        X = column_or_1d(X, warn=True)
        return self._fit(X, y)

    def transform(self, X):
        X = column_or_1d(X, warn=True)
        X = self._transform(X)
        return X.reshape(-1, 1)
