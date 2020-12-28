# config keys
STRUCTLOG_CONFIG_KEY = "STRUCTLOG"
PROCESSOR_NAME_KEY = "PROCESSOR_NAME"
PROCESSOR_OPTIONS_KEY = "PROCESSOR_OPTIONS"
INCLUDE_WORKER_NAME_KEY = "INCLUDE_WORKER_NAME"
PARAMETERS_KEY = "EXTRA_PARAMETERS"

# structlog supported processors
JSON_PROCESSOR = "JSONRenderer"
KEY_VALUE_PROCESSOR = "KeyValueRenderer"

SUPPORTED_PROCESSORS = (JSON_PROCESSOR, KEY_VALUE_PROCESSOR)