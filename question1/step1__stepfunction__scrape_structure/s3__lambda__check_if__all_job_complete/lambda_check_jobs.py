from __future__ import print_function

import json
import boto3

print('Loading function')

batch = boto3.client('batch')

def lambda_handler(event, context):
    # Log the received event
    # print("Received event: " + json.dumps(event, indent=2))
    # Get jobId from the event
    job_ids = event['job_ids']
    print(job_ids)
    try:
        # Call DescribeJobs
        response = batch.describe_jobs(jobs=job_ids)
        # Log response from AWS Batch
        # print("Response: " + json.dumps(response, indent=2))
        # Return the jobtatus
        print(response['jobs'][0]['status'])
        all_success = 'SUCCEEDED'
        for job in response['jobs']:
            print(job['status'])
            if job['status'] == 'FAILED':
                return  'FAILED'
            elif job['status'] != 'SUCCEEDED':
                all_success = "RUNNING"
        # jobStatus = response['jobs'][0]['status']
        return all_success
    except Exception as e:
        print(e)
        message = 'Error getting Batch Job status'
        print(message)
        raise Exception(message)
