import os

import tensorflow as tf
import tensorflow_transform as tft

from modules.transform import FEATURE_KEYS, LABEL_KEY, transformed_name


BATCH_SIZE = 32
NUM_CLASSES = 3


def _input_fn(file_pattern, tf_transform_output, num_epochs, batch_size=BATCH_SIZE):
    transformed_feature_spec = tf_transform_output.transformed_feature_spec()

    def _gzip_reader(filenames):
        return tf.data.TFRecordDataset(filenames, compression_type="GZIP")

    return tf.data.experimental.make_batched_features_dataset(
        file_pattern=file_pattern,
        batch_size=batch_size,
        features=transformed_feature_spec,
        reader=_gzip_reader,
        label_key=transformed_name(LABEL_KEY),
        num_epochs=num_epochs,
        shuffle=True,
    )


def _build_keras_model():
    inputs = {
        transformed_name(key): tf.keras.Input(
            shape=(1,), name=transformed_name(key), dtype=tf.float32
        )
        for key in FEATURE_KEYS
    }

    x = tf.keras.layers.Concatenate()(list(inputs.values()))
    x = tf.keras.layers.Dense(16, activation="relu")(x)
    x = tf.keras.layers.Dense(8, activation="relu")(x)
    outputs = tf.keras.layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=[
            tf.keras.metrics.SparseCategoricalAccuracy(name="accuracy"),
        ],
    )
    return model


def _get_serve_tf_examples_fn(model, tf_transform_output):
    model.tft_layer = tf_transform_output.transform_features_layer()

    @tf.function(
        input_signature=[
            tf.TensorSpec(shape=[None], dtype=tf.string, name="examples")
        ]
    )
    def serve_tf_examples_fn(serialized_tf_examples):
        raw_feature_spec = tf_transform_output.raw_feature_spec()
        raw_feature_spec.pop(LABEL_KEY)

        raw_features = tf.io.parse_example(serialized_tf_examples, raw_feature_spec)
        transformed_features = model.tft_layer(raw_features)
        probabilities = model(transformed_features)

        return {
            "probabilities": probabilities,
            "class_id": tf.argmax(probabilities, axis=1),
        }

    return serve_tf_examples_fn


def run_fn(fn_args):
    tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)

    train_dataset = _input_fn(
        fn_args.train_files,
        tf_transform_output,
        num_epochs=fn_args.custom_config.get("num_epochs", 20),
    )
    eval_dataset = _input_fn(
        fn_args.eval_files,
        tf_transform_output,
        num_epochs=1,
    )

    model = _build_keras_model()
    model.fit(
        train_dataset,
        validation_data=eval_dataset,
        steps_per_epoch=fn_args.train_steps,
        validation_steps=fn_args.eval_steps,
    )

    signatures = {
        "serving_default": _get_serve_tf_examples_fn(
            model, tf_transform_output
        ).get_concrete_function()
    }

    model.save(
        fn_args.serving_model_dir,
        save_format="tf",
        signatures=signatures,
    )
