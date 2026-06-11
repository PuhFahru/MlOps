FROM tensorflow/serving:2.13.0

ENV MODEL_NAME=iris-model

COPY serving_model /models/${MODEL_NAME}
COPY monitoring/prometheus.config /monitoring/prometheus.config

EXPOSE 8501

ENTRYPOINT []
CMD tensorflow_model_server --rest_api_port=8501 --model_name=${MODEL_NAME} --model_base_path=/models/${MODEL_NAME} --monitoring_config_file=/monitoring/prometheus.config
