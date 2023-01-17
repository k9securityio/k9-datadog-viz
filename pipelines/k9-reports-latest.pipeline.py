{'filter': {'query': 'host:("arn:aws:s3:::k9-reports-dev" OR '
                     '"arn:aws:s3:::qm-dev-k9-reports")'},
 'id': '-D4J40aCQLefllk8y9Rh9w',
 'is_enabled': True,
 'is_read_only': False,
 'name': 'k9-reports - latest',
 'processors': [{'grok': {'match_rules': 'parse_filename_metadata '
                                         'customers/%{word:k9.customer.id}/reports/aws/%{number:aws.account.id}/latest/%{notSpace:k9.report.type}\\.latest\\.%{word:k9.file.type}',
                          'support_rules': ''},
                 'is_enabled': True,
                 'name': 'Parse filename metadata - latest',
                 'samples': ['customers/C10001/reports/aws/139710491120/latest/principal-access-summaries.latest.csv',
                             'customers/C10001/reports/aws/139710491120/latest/resource-access-summaries.latest.csv',
                             'customers/C10001/reports/aws/139710491120/latest/principals.latest.csv'],
                 'source': 'aws.s3.key',
                 'type': 'grok-parser'},
                {'is_enabled': True,
                 'is_replace_missing': True,
                 'name': 'Set service to k9',
                 'target': 'service',
                 'template': 'k9',
                 'type': 'string-builder-processor'},
                {'is_enabled': True,
                 'name': 'Remap service to k9',
                 'sources': ['service'],
                 'type': 'service-remapper'},
                {'filter': {'query': '@k9.report.type:"principal-access-summaries"'},
                 'is_enabled': True,
                 'name': 'Filter principal access summaries',
                 'processors': [{'grok': {'match_rules': 'k9_principal_access_summary_rule '
                                                         '%{data:principal_access_summary:csv("analysis_time,principal_name,principal_arn,principal_type,principal_tags,service_name,access_capability,resource_arn")}',
                                          'support_rules': ''},
                                 'is_enabled': True,
                                 'name': 'Parse principal access summary',
                                 'samples': ['2022-12-21T07:15:36.947776+00:00,ci,arn:aws:iam::139710491120:user/ci,IAMUser,"{""BusinessUnit"": '
                                             '""ProductDevelopment""}",Athena,administer-resource,',
                                             '2022-12-21T07:15:36.947776+00:00,ci,arn:aws:iam::139710491120:user/ci,IAMUser,"{""BusinessUnit"": '
                                             '""ProductDevelopment""}",DynamoDB '
                                             'Accelerator '
                                             '(DAX),administer-resource,\n',
                                             '2022-12-21T07:15:36.947776+00:00,ci,arn:aws:iam::139710491120:user/ci,IAMUser,"{""BusinessUnit"": '
                                             '""ProductDevelopment""}",STS,use-resource,arn:aws:iam::139710491120:role/DatadogIntegrationRole'],
                                 'source': 'message',
                                 'type': 'grok-parser'},
                                {'grok': {'match_rules': 'principal_tag_rule '
                                                         '%{data:principal_access_summary.principal_tags:json}',
                                          'support_rules': ''},
                                 'is_enabled': True,
                                 'name': 'Parse principal_tags',
                                 'samples': ['{"k9security:analysis": '
                                             '"include"}'],
                                 'source': 'principal_access_summary.principal_tags',
                                 'type': 'grok-parser'},
                                {'is_enabled': True,
                                 'name': 'Set analysis_time k9 report '
                                         'attribute to official timestamp',
                                 'sources': ['principal_access_summary.analysis_time'],
                                 'type': 'date-remapper'}],
                 'type': 'pipeline'},
                {'filter': {'query': '@k9.report.type:"principals"'},
                 'is_enabled': True,
                 'name': 'Filter principals summary',
                 'processors': [{'grok': {'match_rules': 'k9_principals_summary_rule '
                                                         '%{data:principal_summary:csv("analysis_time,principal_name,principal_arn,principal_type,principal_is_iam_admin,principal_last_used,principal_tag_business_unit,principal_tag_environment,principal_tag_used_by,principal_tags,password_last_used,password_last_rotated,password_state,access_key_1_last_used,access_key_1_last_rotated,access_key_1_state,access_key_2_last_used,access_key_2_last_rotated,access_key_2_state")}',
                                          'support_rules': ''},
                                 'is_enabled': True,
                                 'name': 'Parse principal summary',
                                 'samples': ['2022-12-10T07:14:19.753800+00:00,ci,arn:aws:iam::139710491120:user/ci,IAMUser,True,2022-12-10 '
                                             '05:03:00+00:00,ProductDevelopment,,,"{""BusinessUnit"": '
                                             '""ProductDevelopment""}",,,,2022-12-10 '
                                             '05:03:00+00:00,2021-03-08 '
                                             '21:03:09+00:00,Active,,,\n',
                                             '2022-12-10T07:14:19.753800+00:00,AWSReservedSSO_AdministratorAccess_437be9d757c9ea2f,arn:aws:iam::139710491120:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AdministratorAccess_437be9d757c9ea2f,IAMRole,True,2022-07-21 '
                                             '15:30:39+00:00,,,,{},,,,,,,,,',
                                             '2022-12-10T07:14:19.753800+00:00,datadog-ForwarderStack-1OV25NQJZ3PDG-ForwarderRole-1X48OL78SFSGB,arn:aws:iam::139710491120:role/datadog-ForwarderStack-1OV25NQJZ3PDG-ForwarderRole-1X48OL78SFSGB,IAMRole,False,2022-12-10 '
                                             '05:24:59+00:00,,,,"{""dd_forwarder_version"": '
                                             '""3.40.0""}",,,,,,,,,'],
                                 'source': 'message',
                                 'type': 'grok-parser'},
                                {'grok': {'match_rules': 'principal_tags_rule '
                                                         '%{data:principal_summary.principal_tags:json}',
                                          'support_rules': ''},
                                 'is_enabled': True,
                                 'name': 'Parse principal_tags',
                                 'samples': ['{"k9security:analysis": '
                                             '"include"}',
                                             '{"k9security:analysis": '
                                             '"include", "STAGE": "dev"}'],
                                 'source': 'principal_summary.principal_tags',
                                 'type': 'grok-parser'},
                                {'is_enabled': True,
                                 'name': 'Set analysis_time k9 report '
                                         'attribute to official timestamp',
                                 'sources': ['principal_summary.analysis_time'],
                                 'type': 'date-remapper'}],
                 'type': 'pipeline'},
                {'filter': {'query': '@k9.report.type:"resource-access-summaries"'},
                 'is_enabled': True,
                 'name': 'Filter resource access summaries',
                 'processors': [{'grok': {'match_rules': 'k9_resource_access_summary_rule '
                                                         '%{data:resource_access_summary:csv("analysis_time,service_name,resource_name,resource_arn,access_capability,principal_type,principal_name,principal_arn,resource_tag_confidentiality")}',
                                          'support_rules': ''},
                                 'is_enabled': True,
                                 'name': 'Parse resource access summary',
                                 'samples': ['2022-12-21T07:15:36.947776+00:00,DynamoDB,TerraformStateLock,arn:aws:dynamodb:us-east-1:139710491120:table/TerraformStateLock,administer-resource,IAMUser,ci,arn:aws:iam::139710491120:user/ci,',
                                             '2022-12-21T07:15:36.947776+00:00,DynamoDB,aws-mp-metering-records-dev-skuenzli,arn:aws:dynamodb:us-east-1:139710491120:table/aws-mp-metering-records-dev-skuenzli,administer-resource,IAMUser,ci,arn:aws:iam::139710491120:user/ci,',
                                             '2022-12-21T07:15:36.947776+00:00,KMS,alias/k9-cdk-integration-test,arn:aws:kms:us-east-1:139710491120:key/a71d41d3-d7f2-4829-9d0c-8d527e366a9a,administer-resource,IAMUser,ci,arn:aws:iam::139710491120:user/ci,'],
                                 'source': 'message',
                                 'type': 'grok-parser'},
                                {'is_enabled': True,
                                 'name': 'Set analysis_time k9 report '
                                         'attribute to official timestamp',
                                 'sources': ['resource_access_summary.analysis_time'],
                                 'type': 'date-remapper'}],
                 'type': 'pipeline'},
                {'filter': {'query': '@k9.report.type:"resources"'},
                 'is_enabled': True,
                 'name': 'Filter resources summary',
                 'processors': [{'grok': {'match_rules': 'k9_resource_summary_rule '
                                                         '%{data:resource_summary:csv("analysis_time,resource_name,resource_arn,resource_type,resource_tag_business_unit,resource_tag_environment,resource_tag_owner,resource_tag_confidentiality,resource_tag_integrity,resource_tag_availability,resource_tags")}',
                                          'support_rules': ''},
                                 'is_enabled': True,
                                 'name': 'Parse resources',
                                 'samples': ['2023-01-13T13:14:19.753800+00:00,AccountAdminAccessRole-Sandbox,arn:aws:iam::139710491120:role/AccountAdminAccessRole-Sandbox,IAMRole,,,,,,,{}',
                                             '2023-01-13T13:14:19.753800+00:00,qm-dev-k9-reports,arn:aws:s3:::qm-dev-k9-reports,S3Bucket,,dev,product,,,,"{\'Owner\': '
                                             "'product', 'ManagedBy': "
                                             "'Terraform', 'Environment': "
                                             "'dev', 'Application': 'k9', "
                                             "'Name': "
                                             '\'qm-dev-k9-reports\'}"',
                                             '2023-01-13T13:14:19.753800+00:00,int-test-pg-01,arn:aws:rds:us-east-1:139710491120:cluster:int-test-pg-01,RDSCluster,,,,,,,{}'],
                                 'source': 'message',
                                 'type': 'grok-parser'},
                                {'grok': {'match_rules': 'resource_tags_rule '
                                                         '%{data:resource_summary.resource_tags:json}',
                                          'support_rules': ''},
                                 'is_enabled': True,
                                 'name': 'Parse resource_tags',
                                 'samples': ['{"k9security:analysis": '
                                             '"include"}',
                                             '{"k9security:analysis": '
                                             '"include", "STAGE": "dev"}'],
                                 'source': 'resource_summary.resource_tags',
                                 'type': 'grok-parser'},
                                {'is_enabled': True,
                                 'name': 'Set analysis_time k9 report '
                                         'attribute to official timestamp',
                                 'sources': ['resource_summary.analysis_time'],
                                 'type': 'date-remapper'}],
                 'type': 'pipeline'}],
 'type': 'pipeline'}
