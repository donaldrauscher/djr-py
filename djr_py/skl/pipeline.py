import json

import pandas as pd
import numpy as np

from sklearn.base import clone
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import CountVectorizer

from .select import SelectDocFreq
from .poly import InteractionTerm
from .base import Pipeline
from .util import splitter, flatten


# functions for looking up key in a grouping
def lookup(k, d):
    try:
        return d[k]
    except KeyError:
        return []


def vectorizer(f):
    def wrapper(x, **kwargs):
        return x.apply(f, True, **kwargs)
    return wrapper


@vectorizer
def grouper(x, groups, delimiter='|'):
    x = [lookup(x, groups) for x in splitter(x, delimiter)]
    return delimiter.join(flatten(x))


@vectorizer
def grouper_json(x, groups):
    x = json.loads(x)
    x = [(kk, v) for k, v in x.items() for kk in lookup(k, groups)]
    xx = {}
    for i, j in x:
        try:
            xx[i] += j
        except KeyError:
            xx[i] = j
    return xx


@vectorizer
def jsonify(x, **kwargs):
    return json.loads(x, **kwargs)


# some helper functions for building pipeline
def flex_mask(x, mask, pad):
    x = np.array(x.copy())
    x = np.append(x, np.repeat(pad, len(mask) - len(x)))
    return list(x[mask])


def post_processor(f):
    def wrapper(**kwargs):
        post_process = kwargs.pop('post_process', None)
        steps, feature_names = f(**kwargs)
        if post_process:
            steps.append(('pp', clone(post_process)))
        return Pipeline(steps=steps, fn=feature_names)
    return wrapper


# convert list of dicts into dataframe
def df_json(x, ids, dtype=np.float64):
    keys = np.unique(flatten([i.keys() for i in x]))
    has_extra = (len(np.setdiff1d(keys, ids)) > 0)
    sums = pd.DataFrame(list(x), dtype=dtype).fillna(0).apply(np.sum, axis=1)
    df = pd.DataFrame(list(x), columns=ids, dtype=dtype).fillna(0)
    if has_extra:
        df['OTHER'] = sums - df.apply(np.sum, axis=1)
    return df


# functions for building pipeline
@post_processor
def build_grouper(col, groups, delimiter='|'):
    steps = [
        ('ft', FunctionTransformer(func=lambda x: x[col].fillna(''), validate=False)),
        ('gr', FunctionTransformer(func=grouper, validate=False, kw_args={'groups': groups, 'delimiter': delimiter})),
        ('cv', CountVectorizer(tokenizer=lambda x: splitter(x, delimiter), lowercase=False, min_df=0))
    ]
    feature_names = lambda x: x[2][-1].get_feature_names()
    return steps, feature_names


@post_processor
def build_grouper_json(col, groups, group_ids):
    steps = [
        ('ft', FunctionTransformer(func=lambda x: x[col].fillna('{}'), validate=False)),
        ('gr', FunctionTransformer(func=grouper_json, validate=False, kw_args={'groups': groups})),
        ('pd', FunctionTransformer(func=df_json, validate=False, kw_args={'ids': group_ids})),
        ('cv', SelectDocFreq(min_df=0))
    ]
    feature_names = lambda x: flex_mask(group_ids, x[3][-1].get_support(), 'OTHER')
    return steps, feature_names


@post_processor
def build_json(col, ids):
    steps = [
        ('ft', FunctionTransformer(func=lambda x: x[col].fillna('{}'), validate=False)),
        ('js', FunctionTransformer(func=jsonify, validate=False, kw_args={'parse_float': np.float64})),
        ('pd', FunctionTransformer(func=df_json, validate=False, kw_args={'ids': ids})),
        ('cv', SelectDocFreq(min_df=0))
    ]
    feature_names = lambda x: flex_mask(ids, x[3][-1].get_support(), 'OTHER')
    return steps, feature_names


@post_processor
def build_interaction_term(fe, ia):
    steps = [
        ('it', InteractionTerm(features=fe, interaction=ia)),
        ('cv', SelectDocFreq(min_df=0))
    ]
    feature_names = lambda x: np.array(x[0][-1].get_feature_names())[x[1][-1].get_support()]
    return steps, feature_names
