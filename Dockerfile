FROM python:3.9

WORKDIR /usr/src/restful-booker

COPY . .

RUN pip install requests jsonschema pytest allure-pytest
