
import boto3
import os

dest_aws_access_key_id = os.environ['dest_aws_access_key_id']
dest_aws_secret_access_key = os.environ['dest_aws_secret_access_key']
src_aws_access_key_id = os.environ['src_aws_access_key_id']
src_aws_secret_access_key = os.environ['src_aws_secret_access_key']


src_s3_bucket = 'ext-candidate-data'
target_bucket = 'ext-candidate-data-raw'
s3_src = boto3.client('s3',aws_access_key_id=src_aws_access_key_id, aws_secret_access_key=src_aws_secret_access_key)
s3_target = boto3.client('s3',aws_access_key_id=dest_aws_access_key_id, aws_secret_access_key=dest_aws_secret_access_key)



def main():
        
    paginator = s3_src.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=src_s3_bucket)
    
    objs = []
    for page in pages:
        for obj in page['Contents']:
            objs.append(obj['Key'])
            html_object = s3_src.get_object(Bucket=src_s3_bucket, Key=obj['Key'])
            html = (html_object['Body'].read())
            s3_target.put_object(Body=html, Bucket=target_bucket, Key=obj['Key'])

    return {
        'statusCode': 200,
        'keys': len(objs)
    }

def lambda_handler(event, context):
    return main()
