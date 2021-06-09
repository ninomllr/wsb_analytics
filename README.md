This is a pipeline to track what is happening on /r/wallstreetbets.

Tools used:

- Dagster - Orchestrator - https://dagster.io
- MINIO - S3 data lake - https://min.io
- Delta Lake / Apache Spark - Add SQL functionality to s3
- Jupyter - Notebooks and trying out stuff
- Apache druid - Analytics database
- Apache Superset - Data Visualization

# Run Apache Superset

## build docker image

Because we need to add pydruid for connection to druid.

```
docker build -t superset/druid -f Dockerfile_superset .
```

## How to use this image

#Start a superset instance on port 8080
docker run -d -p 8080:8080 --name superset superset/druid

## Initialize a local Superset Instance

With your local superset container already running...
Setup your local admin account

```
docker exec -it superset superset fab create-admin \
               --username admin \
               --firstname Superset \
               --lastname Admin \
               --email n.mueller@substring.ch \
               --password admin
```

## Migrate local DB to latest

`docker exec -it superset superset db upgrade`

## Load Examples (optional)

`#docker exec -it superset superset load_examples`

## Setup roles

`docker exec -it superset superset init`

## Login and take a look -- navigate to

open http://localhost:8080/login/ -- u/p: [admin/admin]

## catch logs from `stdout`

docker logs superset

## add druid as datasource:

SQLAlchemy URI: `druid://localhost:8888/druid/v2/sql
