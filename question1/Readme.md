#

## Remarks,

There exists a number of permission / IAM configuration,
due to time constraint I did not put it as IAC and configure manually instead.

### HOW to run

1. Because the design consist of step function and I found that step function could not retrieve external s3 bucket. I endup copying all the external raw data to priavte s3 bucket 'ext-candidate-data-raw' , using ext-candidate-data-raw.py for lambda function, trigger manually

2.i go to batch_s3_raw folder to build Docker Image, pushing to destinated ecs
2.ii this will be used as running batch job, with job definition, job queue and compute environments setup

3. create step functions using state_machine.json, replacing corresponding param

4. using state_machin_sample_input.json as template to execution state machine. in which `date` is the date key in external s3 data. assuming the step functions is execute for each date group

5. step function will then group 50 s3 objects as a group, sending to batch job for scraping task, the structured data will be stored in s3 bucket `ext-candidate-data-primary`

6. I was planing to add spark submit job in the end of step function as transformation if I have more time. turns out I make a jupyternotebook to showcase how I perform some basic data transformation.
