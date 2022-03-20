# docker run --env-file .env python-automation-cpt-bid   
# pip freeze > requirements.txt
aws ecr-public get-login-password --region us-east-1 --profile private-tomlee | docker login --username AWS --password-stdin public.ecr.aws/g2g4t0y3
docker build --platform linux/amd64 -t s3-raw-to-s3-primary:latest . --no-cache
docker tag s3-raw-to-s3-primary:latest public.ecr.aws/g2g4t0y3/s3-raw-to-s3-primary:latest
docker push public.ecr.aws/g2g4t0y3/s3-raw-to-s3-primary:latest

# uvicorn main:app --reload   
#  3987  pip freeze > requirements.txt