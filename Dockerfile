FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# copy current directory to the container
COPY . /app

# install dependencies
RUN pip install -r requirements.txt

EXPOSE 80