

import asyncio
import boto3
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import argparse
from botocore.client import Config
from io import StringIO
import datetime as dt

src_s3_bucket = 'ext-candidate-data-raw'
src_aws_access_key_id = os.getenv('SOURCE_S3_ACCESS_KEY')
src_aws_secret_access_key =  os.getenv('SOURCE_S3_SECRET_ACCESS_KEY')

dest_s3_bucket = os.getenv('DEST_S3_BUCKET')
dest_aws_access_key_id = os.getenv('DEST_S3_ACCESS_KEY')
dest_aws_secret_access_key =  os.getenv('DEST_S3_SECRET_ACCESS_KEY')

print(src_aws_access_key_id, src_aws_secret_access_key )
def checkInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def main(object_keys):
    print(src_s3_bucket)
    for object_key in object_keys:
        src_s3 = boto3.client('s3', region_name="ap-northeast-1",aws_access_key_id=dest_aws_access_key_id, aws_secret_access_key=dest_aws_secret_access_key,  config=Config(signature_version='s3v4'))
        dest_s3 =  boto3.client('s3', region_name="ap-northeast-1",aws_access_key_id=dest_aws_access_key_id, aws_secret_access_key=dest_aws_secret_access_key,  config=Config(signature_version='s3v4'))
        # paginator = dest_s3.get_paginator('list_objects_v2')
        # pages = paginator.paginate(Bucket=dest_s3_bucket)
        # objct_key = 'raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=0'
        # src_s3.download_file(src_s3_bucket, objct_key, 'temp2.html')

      
        # i = 0
        # for page in pages:
        #     for obj in page['Contents']:
        #         if i ==0:
        #             print(obj['Key'])
        #             i = 1
                # print(obj['Size'])


        # print(objct_key)
        obj = src_s3.get_object(Bucket=src_s3_bucket, Key=object_key)
        html = (obj['Body'].read())

        soup = BeautifulSoup(html, 'lxml') 
        # regex = re.compile(' resultWithShelf ')

        jobs = soup.find_all('a', class_="resultWithShelf")
        

        data = []

        # job title salary

        for job in jobs:
            salary_snippet = job.find('span', class_ ='salary-snippet', text=True)
            raw_salary_snippet = salary_snippet.string if salary_snippet else None

            salary_range = None
            salary_period = None
            salary_from = None
            salary_to = None
            salary_fixed = None
            if raw_salary_snippet is not None:
                salary_snippet = raw_salary_snippet.replace('$', '').replace(',', '')

                if salary_snippet.endswith('an hour'):
                    salary_period = 'hourly'
                elif salary_snippet.endswith('a week'):
                    salary_period = 'weekly'
                elif salary_snippet.endswith('a day'):
                    salary_period = 'dayly'
                elif salary_snippet.endswith('a year'):
                    salary_period = 'yearly'
                else:
                    print('unknown',salary_snippet)
                
                salary_snippet = salary_snippet.replace('an hour', '').replace('a week', '').replace('a year', '').replace('a day', '').strip()
                
                
                if salary_snippet.startswith('Up to'):
                    salary_range = 'upto'
                    salary_to = salary_snippet.replace('Up to', '').strip()
                elif salary_snippet.startswith('From'):
                    salary_range = 'from'
                    salary_from = salary_snippet.replace('From', '').strip()
                elif len(salary_snippet.split(' - ')) == 2:
                    salary_range = 'range'
                    [salary_from, salary_to] = salary_snippet.split(' - ')
                elif checkInt(salary_snippet):
                    salary_range = 'fixed'
                    salary_fixed = salary_snippet
                else:
                    print('unknown',salary_snippet)

                # print(salary_snippet)
            # print(salary_snippet)


            title = job.find('h2', class_='jobTitle').find_all('span')[-1].string
            
            company_name = job.find('span', class_='companyName').string
            company_location = job.find('div', class_='companyLocation').string

            data.append([dt.datetime.now(),title, company_name, company_location, raw_salary_snippet, salary_range, salary_period, salary_from, salary_to, salary_fixed ]  )

        # first_job = jobs[0]
        
        # salary_snippet = first_job.find('span', class_ ='salary-snippet').string
        # print(salary_snippet)
        
        df = pd.DataFrame(data, columns=['Create At', 'Title', 'Company', 'Location', 'Salary Snippet', 'Salary Range', 'Salary Period', 'Salary From', 'Salary To', 'Salary Fixed' ])
        csv_buffer = StringIO()
        # print(df)
        df.to_csv(csv_buffer)
        # s3_resource = boto3.resource('s3')
        dest_s3.put_object(Body=csv_buffer.getvalue(), Bucket=dest_s3_bucket, Key=f'{object_key}.csv')
        # df.to_csv('file_name.csv')

# df.to_csv('file_name.csv', index=False)

    # print(soup.prettify())
if __name__ == '__main__':
    import urllib.parse
    # xx = urllib.parse.quote_plus('raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=0')
    # print(xx)
    parser = argparse.ArgumentParser()
    parser.add_argument('--object-key', action='append')

    #raw%2F2021-08-28%2Fjobs%3Fq%3Dconstruction%2520worker%26sort%3Ddate%26limit%3D50%26fromage%3D1%26start%3D0

    object_keys = ['raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=0']
    for key, value in parser.parse_args()._get_kwargs():
        if value is not None:
            print(key)
            if key == 'object_key':
                print(value)
                object_keys = value
            # print(key, value)
    object_keys = [ urllib.parse.unquote_plus(object_key).replace(' ', '%20') for object_key in object_keys]
    print(object_keys)
    main(object_keys)
    # asyncio.run(main(object_keys))  



###
#  "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=0",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=100",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1000",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1050",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1100",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1150",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1200",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1250",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1300",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1350",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1400",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1450",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=150",
#     "raw/2021-08-28/jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=1500",
###