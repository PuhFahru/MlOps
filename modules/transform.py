import tensorflow as tf
import tensorflow_transform as tft


LABEL_KEY = "species"
FEATURE_KEYS = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]


def transformed_name(key):
    return key + "_xf"


def preprocessing_fn(inputs):
    """Preprocess raw Iris features for model training."""
    outputs = {}

    for key in FEATURE_KEYS:
        outputs[transformed_name(key)] = tft.scale_to_z_score(
            tf.cast(inputs[key], tf.float32)
        )

    outputs[transformed_name(LABEL_KEY)] = tf.cast(inputs[LABEL_KEY], tf.int64)
    return outputs
