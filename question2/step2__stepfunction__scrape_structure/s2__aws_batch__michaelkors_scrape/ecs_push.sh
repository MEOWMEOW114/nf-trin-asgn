aws ecr-public get-login-password --region us-east-1 --profile private-tomlee | docker login --username AWS --password-stdin public.ecr.aws/g2g4t0y3
docker build --platform linux/amd64 -t nft-michaelkors-scrape:latest . --no-cache
docker tag nft-michaelkors-scrape:latest public.ecr.aws/g2g4t0y3/nft-michaelkors-scrape:latest
docker push public.ecr.aws/g2g4t0y3/nft-michaelkors-scrape:latest