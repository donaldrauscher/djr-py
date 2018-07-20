from sklearn.feature_selection import SelectKBest as BaseSelectKBest
from sklearn.pipeline import FeatureUnion


# allow k to be larger than X (equivalent of k='all')
class SelectKBest(BaseSelectKBest):
    def _check_params(self, X, y):
        pass


# feature union of iid estimators (allows setting hyperparameter identically across all estimators)
class FeatureUnionIID(FeatureUnion):
    def set_params(self, **kwargs):
        for _, t in self.transformer_list:
            t.set_params(**kwargs)
