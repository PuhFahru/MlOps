import os

import tensorflow_model_analysis as tfma
from tfx.components import (
    CsvExampleGen,
    Evaluator,
    ExampleValidator,
    Pusher,
    SchemaGen,
    StatisticsGen,
    Trainer,
    Transform,
)
from tfx.dsl.components.common.resolver import Resolver
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.orchestration import pipeline
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner
from tfx.orchestration.metadata import sqlite_metadata_connection_config
from tfx.proto import pusher_pb2, trainer_pb2
from tfx.types import Channel
from tfx.types.standard_artifacts import Model, ModelBlessing


PIPELINE_NAME = "fahrual_19"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_ROOT = os.path.join(BASE_DIR, "fahrual_19-pipeline")
METADATA_PATH = os.path.join(PIPELINE_ROOT, "beam_metadata.sqlite")
DATA_ROOT = os.path.join(BASE_DIR, "data")
TRANSFORM_MODULE = os.path.join(BASE_DIR, "modules", "transform.py")
TRAINER_MODULE = os.path.join(BASE_DIR, "modules", "trainer.py")
SERVING_MODEL_DIR = os.path.join(BASE_DIR, "serving_model")


def _create_pipeline():
    example_gen = CsvExampleGen(input_base=DATA_ROOT)

    statistics_gen = StatisticsGen(examples=example_gen.outputs["examples"])

    schema_gen = SchemaGen(
        statistics=statistics_gen.outputs["statistics"],
        infer_feature_shape=True,
    )

    example_validator = ExampleValidator(
        statistics=statistics_gen.outputs["statistics"],
        schema=schema_gen.outputs["schema"],
    )

    transform = Transform(
        examples=example_gen.outputs["examples"],
        schema=schema_gen.outputs["schema"],
        module_file=TRANSFORM_MODULE,
    )

    trainer = Trainer(
        module_file=TRAINER_MODULE,
        examples=transform.outputs["transformed_examples"],
        transform_graph=transform.outputs["transform_graph"],
        schema=schema_gen.outputs["schema"],
        train_args=trainer_pb2.TrainArgs(num_steps=20),
        eval_args=trainer_pb2.EvalArgs(num_steps=5),
        custom_config={"num_epochs": 30},
    )

    model_resolver = Resolver(
        strategy_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
        model=Channel(type=Model),
        model_blessing=Channel(type=ModelBlessing),
    ).with_id("latest_blessed_model_resolver")

    eval_config = tfma.EvalConfig(
        model_specs=[tfma.ModelSpec(label_key="species")],
        slicing_specs=[tfma.SlicingSpec()],
        metrics_specs=[
            tfma.MetricsSpec(
                metrics=[
                    tfma.MetricConfig(
                        class_name="SparseCategoricalAccuracy",
                        threshold=tfma.MetricThreshold(
                            value_threshold=tfma.GenericValueThreshold(
                                lower_bound={"value": 0.5}
                            )
                        ),
                    ),
                    tfma.MetricConfig(class_name="ExampleCount"),
                ]
            )
        ],
    )

    evaluator = Evaluator(
        examples=example_gen.outputs["examples"],
        model=trainer.outputs["model"],
        baseline_model=model_resolver.outputs["model"],
        eval_config=eval_config,
    )

    pusher = Pusher(
        model=trainer.outputs["model"],
        model_blessing=evaluator.outputs["blessing"],
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(
                base_directory=SERVING_MODEL_DIR
            )
        ),
    )

    return pipeline.Pipeline(
        pipeline_name=PIPELINE_NAME,
        pipeline_root=PIPELINE_ROOT,
        components=[
            example_gen,
            statistics_gen,
            schema_gen,
            example_validator,
            transform,
            trainer,
            model_resolver,
            evaluator,
            pusher,
        ],
        metadata_connection_config=sqlite_metadata_connection_config(METADATA_PATH),
        enable_cache=False,
        beam_pipeline_args=[
            "--direct_running_mode=in_memory",
            "--direct_num_workers=1",
        ],
    )


if __name__ == "__main__":
    BeamDagRunner().run(_create_pipeline())
