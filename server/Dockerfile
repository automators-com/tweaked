# Use base python image
FROM python:3.12
# Install pg_dump
RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /code

# copy requirements.txt
COPY ./requirements.txt /code/requirements.txt

# install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy the app
COPY . /code/app

# run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
