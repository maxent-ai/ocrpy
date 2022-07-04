import yaml
from attr import field, define

__all__ = ["PipelineConfig"]


@define
class PipelineConfig:
    """
    OCR Pipeline Configuration container.

    Attributes
    ----------
    config_path : str
        Path to the ocrpy config file.

    example config file:
    ---------------------
    storage_config:
        source_dir: /path/to/source/dir
        destination_dir: /path/to/destination/dir
    parser_config:
        parser_backend: pytesseract
    cloud_credentials:
        aws: /path/to/aws-credentials.env
        gcp: /path/to/gcp-credentials.json
    """

    config_path = field()
    pipeline_configuration = field(init=False, repr=False)

    def __attrs_post_init__(self):
        config = self._load_config()
        self._validate_config(config)
        self.pipeline_configuration = self._to_pipeline_config(config)

    def _load_config(self):
        with open(self.config_path) as f:
            config = yaml.safe_load(f)
        return config

    def _validate_config(self, config):
        if "storage_config" not in config.keys():
            raise ValueError(
                "Missing Storage config - Please provide the storage_config with `source_dir` and `destination_dir` params."
            )
        elif "parser_config" not in config.keys():
            raise ValueError(
                "Missing Parser config - Please provide the parser_config with `parser_backend` param set to one of these: 'pytesseract', 'aws-textract' or 'google-cloud-vision'"
            )
        elif "cloud_credentials" not in config.keys():
            raise ValueError(
                "Missing cloud config - Please provide appropriate cloud credentials path to `aws` or `gcp`. if not using any cloud leave these params empty."
            )

    def _to_pipeline_config(self, config):
        source_dir = config["storage_config"]["source_dir"]
        destination_dir = config["storage_config"]["destination_dir"]
        parser_backend = config["parser_config"]["parser_backend"]
        creds = config["cloud_credentials"]
        aws_creds = creds["aws"]
        gcp_creds = creds["gcp"]
        if not aws_creds:
            aws_creds = ""
        if not gcp_creds:
            gcp_creds = ""
        return dict(
            source_dir=source_dir,
            destination_dir=destination_dir,
            parser_backend=parser_backend,
            credentials_config={"AWS": aws_creds, "GCP": gcp_creds},
        )
