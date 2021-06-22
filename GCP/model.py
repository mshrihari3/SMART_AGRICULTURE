from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)

CSV_COLUMNS = 'LUX,Temperature,Humidity,Moisture,a,b,c,e,y,nony,final'.split(',')
LABEL_COLUMN = 'final'
DEFAULTS = [[8000],[27],[41],[756],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0]]

INPUT_COLUMNS = [
    tf.feature_column.numeric_column('LUX'),
    tf.feature_column.numeric_column('Temperature'),
    tf.feature_column.numeric_column('Humidity'),
    tf.feature_column.numeric_column('Moisture'),
    tf.feature_column.numeric_column('a'),
    tf.feature_column.numeric_column('b'),
    tf.feature_column.numeric_column('c'),
    tf.feature_column.numeric_column('e'),
    tf.feature_column.numeric_column('y'),
    tf.feature_column.numeric_column('nony')
    ]

def build_estimator(model_dir, nbuckets, hidden_units):
    estimator = tf.estimator.DNNClassifier(
        model_dir = model_dir,
        feature_columns=INPUT_COLUMNS,
        hidden_units=[10,10],
        n_classes=2
        )

    # add extra evaluation metric for hyperparameter tuning
    estimator = tf.compat.v1.estimator.add_metrics(estimator, add_eval_metrics)
    return estimator

def add_eval_metrics(labels, predictions):
    auc_metric = tf.keras.metrics.AUC(name="my_auc")
    auc_metric.update_state(y_true=labels, y_pred=predictions['logistic'])
    return {'auc': auc_metric}

def add_engineered(features):
    return features

def serving_input_fn():
    feature_placeholders = {
        # All the real-valued columns
        column.name: tf.compat.v1.placeholder(tf.float64, [None]) for column in INPUT_COLUMNS
    }
    features = add_engineered(feature_placeholders.copy())
    return tf.estimator.export.ServingInputReceiver(features, feature_placeholders)

def read_dataset(filename, mode, batch_size = 128):
    def _input_fn():
        def decode_csv(value_column):
            columns = tf.compat.v1.decode_csv(value_column, record_defaults = DEFAULTS)
            features = dict(zip(CSV_COLUMNS, columns))
            label = features.pop(LABEL_COLUMN)
            return add_engineered(features), label

        # Create list of files that match pattern
        file_list = tf.compat.v1.gfile.Glob(filename)

        # Create dataset from file list
        dataset = tf.compat.v1.data.TextLineDataset(file_list).map(decode_csv)

        if mode == tf.estimator.ModeKeys.TRAIN:
            num_epochs = None # indefinitely
            dataset = dataset.shuffle(buffer_size = 10 * batch_size)
        else:
            num_epochs = 1 # end-of-input after this

        dataset = dataset.repeat(num_epochs).batch(batch_size)
        batch_features, batch_labels = dataset.make_one_shot_iterator().get_next()
        return batch_features, batch_labels
    return _input_fn

def train_and_evaluate(args):
    tf.compat.v1.summary.FileWriterCache.clear() # ensure filewriter cache is clear for TensorBoard events file
    estimator = build_estimator(args['output_dir'], args['nbuckets'], args['hidden_units'].split(' '))
    train_spec = tf.estimator.TrainSpec(
        input_fn = read_dataset(
            filename = args['train_data_paths'],
            mode = tf.estimator.ModeKeys.TRAIN,
            batch_size = args['train_batch_size']),
        max_steps = args['train_steps'])
    exporter = tf.estimator.LatestExporter('exporter', serving_input_fn)
    eval_spec = tf.estimator.EvalSpec(
        input_fn = read_dataset(
            filename = args['eval_data_paths'],
            mode = tf.estimator.ModeKeys.EVAL,
            batch_size = args['eval_batch_size']),
        steps = 100,
        exporters = exporter)
    tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)

def gzip_reader_fn():
    return tf.TFRecordReader(options=tf.python_io.TFRecordOptions(
            compression_type = tf.python_io.TFRecordCompressionType.GZIP))

def generate_tfrecord_input_fn(data_paths, num_epochs = None, batch_size = 128, mode = tf.estimator.ModeKeys.TRAIN):
    def get_input_features():
        # Read the tfrecords. Same input schema as in preprocess
        input_schema = {}
        if mode != tf.estimator.ModeKeys.INFER:
            input_schema[LABEL_COLUMN] = tf.FixedLenFeature(shape = [1], dtype = tf.float64, default_value = 0.0)
        for name in ['LUX','Temperature','Humidity','Moisture','a','b','c','e','y','nony']:
            input_schema[name] = tf.FixedLenFeature(shape = [1,], dtype = tf.float64, default_value = 'null')
        # How?
        keys, features = tf.contrib.learn.io.read_keyed_batch_features(
            data_paths[0] if len(data_paths) == 1 else data_paths,
            batch_size,
            input_schema,
            reader = gzip_reader_fn,
            reader_num_threads = 4,
            queue_capacity = batch_size * 2,
            randomize_input = (mode != tf.estimator.ModeKeys.EVAL),
            num_epochs = (1 if mode == tf.estimator.ModeKeys.EVAL else num_epochs))
        target = features.pop(LABEL_COLUMN)
        features[KEY_FEATURE_COLUMN] = keys
        return add_engineered(features), target

    # Return a function to input the features into the model from a data path.
    return get_input_features