from dagster import pipeline, repository, schedule, solid
import requests
import boto3
from datetime import datetime

@solid
def upload_s3(context, content):
    timestampStr = datetime.now().strftime("%Y%m%d%H%M%S")

    context.log.info(content)
    s3 = boto3.resource(
    's3',
    region_name='us-east-1',
    endpoint_url='http://minio:9000/',
    aws_access_key_id="AKIAWSB",
    aws_secret_access_key="WSBSECRETKEY"
    )
    s3.Object('wallstreetbets', timestampStr+'.json').put(Body=content)

@solid
def load_url(context):
    r = requests.get('https://www.reddit.com/r/wallstreetbets.json', headers = {'User-agent': 'dagster-bot 0.1'})
    return r.text

@pipeline
def load_wsb():
    upload_s3(load_url())

@schedule(cron_schedule="* * * * *", pipeline_name="load_wsb", execution_timezone="US/Central")
def my_wsb_load_schedule(_context):
    return {}


@repository
def deploy_docker_repository():
    return [load_wsb, my_wsb_load_schedule]
