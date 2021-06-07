from dagster import resource, Field
import boto3


class Boto3Connector(object):
    def __init__(self, aws_access_key_id, aws_secret_access_key, endpoint_url, region_key):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_key = region_key

    def get_client(self):
        s3_client = boto3.resource(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.endpoint_url,
        )

        return s3_client


@resource(
    config_schema={
        'aws_access_key_id': Field(str),
        'aws_secret_access_key': Field(str),
        'endpoint_url': Field(str),
        'region_key': Field(str),
    }
)
def boto3_connection(context):
    return Boto3Connector(
        context.resource_config['aws_access_key_id'],
        context.resource_config['aws_secret_access_key'],
        context.resource_config['endpoint_url'],
        context.resource_config['region_key'],
    )
