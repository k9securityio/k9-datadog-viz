"""
Get a pipeline returns "OK" response
"""
import json

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.logs_pipelines_api import LogsPipelinesApi

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = LogsPipelinesApi(api_client)
    # response = api_instance.list_logs_pipelines()
    # print(response)
    response = api_instance.get_logs_pipeline(
        pipeline_id="-D4J40aCQLefllk8y9Rh9w",
    )

    print(response)
