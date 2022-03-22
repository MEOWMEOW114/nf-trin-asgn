## design diagrams

### 1. s[1] cloudwatch/event Bridge trigger step function as etl every hour

### 2. s[2] step function for ETL

2. step function detail is in step_function\_\_state_machine.md
3. step function will create a batch job for download the raw content as cach, based on category data.
4. use selenium to scrape html data from website , storing as raw data
5. use beautifulsoup to parse the html data
6.

### 3. s[3] mannual step to trigger EMR job

- for aggenration / further transformation of data base on ex

## DataStore

### 1. company metadata

- sample of category data company*metadata = {
  'michaelkors_global': {
  'woman/handbags': 'https://www.michaelkors.global/en_HK/women/handbags/*/N-1ysakls'
  }
  }

- to be stored in S3 / dynamodb / mongodb
- definition of companies and categories for scraping
- in future you could add more items into cateogyr, athe the batch job will trigger 1 job for webcontent as crawling for each url, in each company

### 2. raw data (html content)

- s3 bucket nft-question2-scraping-raw
- level:
  <date> --> <company> --> <category>

- for example
  s3://2022/03/22/michaelkors_global/woman/handbags/source.html

### 3. primary data ( about scraping from html)

- s3 bucket nft-question2-scraping-primary

### 4. nft-question2-scraping-transformed ( after EMR processing)

- to be in batch job, now it is mannual trigger

- use <s3 nft-question2-scraping-primary> as input
- --> < spark job >
- output stored in <s3 nft-question2-scraping-transformed>
