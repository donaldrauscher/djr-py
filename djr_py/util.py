import numpy as np
import pandas as pd

from scipy import sparse


# general stuff
splitter = lambda x, y: [] if x == '' else x.split(y)
flatten = lambda l: [item for sublist in l for item in sublist]


# some functions for dealing with parameter grids
def add_prefix(prefix, x, split='__'):
    if isinstance(x, dict):
        return {'{}{}{}'.format(prefix, split, k): v for k, v in x.items()}
    return ['{}{}{}'.format(prefix, split, i) for i in x]


def safe_partition(x, split='__'):
    x2 = x.partition(split)
    if x2[2] != '':
        return x2[2]
    return x


def remove_prefix(x, split='__'):
    if isinstance(x, dict):
        return {safe_partition(k, split): v for k, v in x.items()}
    return [i.partition(split)[2] for i in x]


def flatten_dict(x, split='__'):
    temp = {}
    for k, v in x.items():
        if isinstance(v, dict):
            temp.update(add_prefix(k, flatten_dict(v.copy()), split=split))
        else:
            temp.update({k: v})
    return temp


# return first non-null value in array
# pylint: disable=invalid-unary-operand-type
def first_non_null(x):
    if x.ndim > 1:
        raise ValueError
    if np.sum(~pd.isnull(x)) > 0:
        return x[np.min(np.where(~pd.isnull(x)))]
    return np.nan


# safe divide
def safe_divide(x, y, impute=0):
    try:
        return x/y
    except ZeroDivisionError:
        return impute


# applies a function to each element in a matrix
def element_wise(X, fn, *arg, **kwargs):
    if sparse.isspmatrix(X):
        X.data = np.vectorize(fn)(X.data, *arg, **kwargs)
        return X
    return np.vectorize(fn)(X, *arg, **kwargs)
