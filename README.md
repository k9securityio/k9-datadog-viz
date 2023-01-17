# k9 Security Datadog Integration

## Get the log pipeline

```shell
export DD_PIPELINE_ID="-D4J40aCQLefllk8y9Rh9w" # 'k9-reports - latest' pipeline 
curl -X GET "https://api.datadoghq.com/api/v1/logs/config/pipelines/${DD_PIPELINE_ID}" \
     -H "Accept: application/json" -H "DD-API-KEY: ${DD_API_KEY}" -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
     | tee pipelines/k9-reports-latest.pipeline.json
```