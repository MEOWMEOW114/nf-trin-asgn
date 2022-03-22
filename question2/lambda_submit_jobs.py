from __future__ import print_function

import json
import boto3
company_metadata = {
    'michaelkors_global': {
        'woman/handbags': 'https://www.michaelkors.global/en_HK/women/handbags/_/N-1ysakls'
    }
}
# print('Loading function')
batch = boto3.client('batch')
def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))
    # Get parameters for the SubmitJob call
    # http://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html
    jobName = event['jobName']
    # jobQueue = event['jobQueue']
    # jobDefinition = event['jobDefinition']
    
    
    job_ids = []
    job_definition = 'nft-question2-kros-scraping'
    job_queue = 'NftQuestion1JobQueue'
    
    for company, metadata in company_metadata.items():
        for category, url in metadata.items():

        
            commands = ["python3",'scrape.py', '--company', company, '--category', category ]
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
