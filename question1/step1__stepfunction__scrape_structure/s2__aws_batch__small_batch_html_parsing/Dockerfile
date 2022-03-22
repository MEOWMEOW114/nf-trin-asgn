# creates a layer from the python:3 Docker image
FROM python:3.10-slim-buster 

# copy and install dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt

# add script
COPY bs.py .
# EXPOSE 8000:8000

# define the command to run the script
# CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]

