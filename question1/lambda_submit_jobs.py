from __future__ import print_function

import json
import boto3
import urllib.parse
import os
aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key']


# print('Loading function')
batch = boto3.client('batch')
def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))
    # Get parameters for the SubmitJob call
    # http://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html
    jobName = event['jobName']
    date_string = event['date']
    date_string = f"raw/{date_string}"
    # jobQueue = event['jobQueue']
    # jobDefinition = event['jobDefinition']
    
    
    job_ids = []
    job_definition = 'parse-s3-html-for-1-page'
    job_queue = 'NftQuestion1JobQueue'
    
    source_bucket = 'ext-candidate-data-raw'
    target_bucket = 'ext-candidate-data-primary'
    s3 = boto3.client('s3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    paginator = s3.get_paginator('list_objects_v2')
    print(date_string)
    pages = paginator.paginate(Bucket=source_bucket, PaginationConfig={'PageSize': 50}, Prefix=date_string)
   
    for page in pages:
        
        commands = ["python",'bs.py']
        objs = []
        for obj in page['Contents']:
            commands.append('--object-key')
            commands.append(urllib.parse.quote_plus(obj['Key']))
            # print(commands)
            objs.append(obj['Key'])
        print(commands)
        parameters = {}
        containerOverrides={
            "command": commands
        }

    
        try:
            # Submit a Batch Job
            response = batch.submit_job(
                jobQueue=job_queue,
                jobName=jobName,
                jobDefinition=job_definition,
                containerOverrides=containerOverrides)
            # Log response from AWS Batch
            print("Response: " + json.dumps(response, indent=2))
            # Return the jobId
            jobId = response['jobId']
            job_ids.append(jobId)
           
        except Exception as e:
            print(e)
            message = 'Error submitting Batch Job'
            print(message)
            # raise Exception(message)

    return {
        'job_ids': job_ids
    }