from dagster import (
    pipeline,
    repository,
    schedule,
    solid,
    file_relative_path,
    ModeDefinition,
    PresetDefinition)
import requests
import boto3
from common.resources import boto3_connection
from datetime import datetime

local_mode = ModeDefinition(
    name="local",
    resource_defs={
        'boto3': boto3_connection,
    },
)


@solid(required_resource_keys={'boto3'}, description='''Uploads file to s3 ''')
def upload_s3(context, content):
    timestampStr = datetime.now().strftime("%Y%m%d%H%M%S")
    s3 = context.resources.boto3.get_client()
    s3.Object('lake', 'wallstreetbets/'+timestampStr+'.json').put(Body=content)


@solid
def load_url(context):
    r = requests.get('https://www.reddit.com/r/wallstreetbets.json',
                     headers={'User-agent': 'dagster-bot 0.1'})
    return r.text


@pipeline(
    mode_defs=[local_mode],
    preset_defs=[
        PresetDefinition.from_files(
            name='local',
            mode='local',
            config_files=[
                file_relative_path(
                    __file__, 'environments/localhost.yaml'),
            ],
        ),
    ],
)
def load_wsb():
    upload_s3(load_url())


@schedule(
    cron_schedule="* * * * *",
    pipeline_name="load_wsb",
    execution_timezone="US/Central",
    mode="local")
def my_wsb_load_schedule(_context):
    return {'resources': {'boto3': {'config': {'aws_access_key_id': 'AKIAWSB', 'aws_secret_access_key': 'WSBSECRETKEY', 'endpoint_url': 'http://minio:9000', 'region_key': 'us-east-1'}}}}


@repository
def deploy_docker_repository():
    return [load_wsb, my_wsb_load_schedule]
