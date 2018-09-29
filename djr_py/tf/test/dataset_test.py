import pandas as pd
import tensorflow as tf

from ..dataset import make_tf_records, fetch_tf_records


# compare dataframes
def test_tf_records(tmpdir):

    # create df and export as tfrecords
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    tmpfile = str(tmpdir.join('test.tfrecord'))
    make_tf_records(df, tmpfile)

    # import tfrecords
    feature_spec = {
        'col1': tf.FixedLenFeature(shape=[1], dtype=tf.int64),
        'col2': tf.FixedLenFeature(shape=[1], dtype=tf.string)
    }

    records = fetch_tf_records(tmpfile, feature_spec)
    for k in records.keys():
        records[k] = records[k].flatten()

    df2 = pd.DataFrame(records)
    df2['col2'] = df2.col2.apply(lambda x: x.decode('utf-8'))

    # compare
    assert df.equals(df2)
