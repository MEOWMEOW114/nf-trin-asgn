import asyncio
import boto3
import os

from dotenv import load_dotenv
load_dotenv()


async def main():
    dest_s3_bucket = os.getenv('DEST_S3_BUCKET')
    dest_aws_access_key_id = os.getenv('DEST_S3_ACCESS_KEY')
    dest_aws_secret_access_key =  os.getenv('DEST_S3_SECRET_ACCESS_KEY')
    dest_s3_primary_bucket = 'nft-question2-scraping-primary'

if __name__ == '__main__':
    asyncio.run(main())  
