from sklearn.externals.joblib import register_parallel_backend

from .util import add_prefix, remove_prefix, flatten_dict, first_non_null, safe_divide, element_wise, splitter

from .skl.stack import StackingClassifier, StackingRegressor
from .skl.preprocessing import SelectKBest, FeatureUnionIID
from .skl.select import SelectDocFreq
from .skl.label import LabelEncoder
from .skl.lognormal import LogNormalTransformer, LogNormalTransformer1D
from .skl.parallel import MultiprocessingBackendDill
from .skl.pipeline import build_grouper, build_grouper_json, build_json, build_interaction_term
from .skl.poly import PolynomialFeatures, InteractionTerm

# make multiprocessing backend using dill the default for `Parallel`
register_parallel_backend('multiprocessing', MultiprocessingBackendDill, make_default=True)
