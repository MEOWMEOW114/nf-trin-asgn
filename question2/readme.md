## design diagrams

1. cloudwatch trigger step function as etl every hour
2. step function detail is in step_function\_\_state_machine.md
3. step function will create a batch job for download the raw content as cach, based on category data.
4. sample of category data company*metadata = {
   'michaelkors_global': {
   'woman/handbags': 'https://www.michaelkors.global/en_HK/women/handbags/*/N-1ysakls'
   }
   }

in future you could add more items into cateogyr, athe the batch job will trigger 1 job for webcontent as crawling for each url, in each company

5. crawling code is in aws_batch\_\_michaelkors_scrape folder, with pagination support
