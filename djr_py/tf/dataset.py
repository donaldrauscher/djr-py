import glob
import tensorflow as tf


# convert pandas dataframe into tfrecords file
def make_tf_records(df, out):
    field_types = dict(df.dtypes)
    records = df.to_dict(orient='records')

    with tf.python_io.TFRecordWriter(out) as writer:
        for row in records:
            features = {}
            for k, v in row.items():
                if field_types[k] == 'int64':
                    features[k] = tf.train.Feature(int64_list=tf.train.Int64List(value=[v]))
                elif field_types[k] == 'float64':
                    features[k] = tf.train.Feature(float_list=tf.train.FloatList(value=[v]))
                else:
                    features[k] = tf.train.Feature(bytes_list=tf.train.BytesList(value=[str(v).encode('utf-8')]))

            example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(example.SerializeToString())


# loads entire tfrecords file
def fetch_tf_records(input_file_pattern, feature_spec, top=None):
    def input_fn():
        input_filenames = glob.glob(input_file_pattern)

        if not top:
            n = 0
            for f in input_filenames:
                n += sum(1 for _ in tf.python_io.tf_record_iterator(f))
        else:
            n = top

        ds = tf.data.TFRecordDataset(input_filenames)
        ds = ds.map(lambda x: tf.parse_single_example(x, feature_spec))
        ds = ds.batch(n).repeat(1)

        return ds.make_one_shot_iterator().get_next()

    with tf.Session() as sess:
        return sess.run(input_fn())
