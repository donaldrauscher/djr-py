import abc

import numpy as np

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LogisticRegression, LinearRegression

# pylint: disable=no-name-in-module
from scipy.special import logit

from ..util import add_prefix


# chop off the first column
def chop_col0(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)[:, 1:]
    return wrapper


# convert 1d output to 2d output
def to_2d(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).reshape(-1, 1)
    return wrapper


# NOTE: need to add to instance AND class so `clone` in `cross_val_predict` works
def add_transform(estimator, fn, wrapper=lambda x: x):
    if isinstance(estimator, Pipeline):
        estimator = estimator.steps[-1][-1]
    estimator.transform = wrapper(getattr(estimator, fn))
    estimator.__class__.transform = wrapper(getattr(estimator.__class__, fn))


# stacking base
class StackingBase(Pipeline):

    # pylint: disable=super-init-not-called
    def __init__(self, estimators, cv=3):
        self.estimators = estimators
        self._add_transform()
        self.meta = self._meta()
        self.cv = cv
        self.steps = [('stack', FeatureUnion(self.estimators)), ('meta', self.meta)]
        self.memory = None

    @abc.abstractmethod
    def _meta(self):
        pass

    @abc.abstractmethod
    def _add_transform(self):
        pass

    def _validate_steps(self):
        pass

    def set_params(self, **kwargs):
        return super(StackingBase, self).set_params(**add_prefix('stack', kwargs))

    # pylint: disable=arguments-differ
    def fit(self, X, y):
        meta_features = cross_val_predict(FeatureUnion(self.estimators), X, y, cv=self.cv, method="transform")
        self.meta.fit(meta_features, y)
        for _, estimator in self.estimators:
            estimator.fit(X, y)
        return self


# stacking classifier
class StackingClassifier(StackingBase):

    # default function applies logit to probabilies and applies logistic regression
    def _meta(self):
        return Pipeline([
            ('logit', FunctionTransformer(lambda x: logit(np.clip(x, 0.001, 0.999)))),
            ('scaler', StandardScaler()),
            ('lr', LogisticRegression())
        ])

    def _add_transform(self):
        for _, estimator in self.estimators:
            add_transform(estimator, 'predict_proba', chop_col0)


# stacking regressor
class StackingRegressor(StackingBase):

    def _meta(self):
        return LinearRegression()

    def _add_transform(self):
        for _, estimator in self.estimators:
            add_transform(estimator, 'predict', to_2d)
