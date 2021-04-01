# Tests for restful-booker
[Restful booker](http://restful-booker.herokuapp.com/) is a public api.

I am learning pytest and how automate api. These tests are just my practice.

## Run without docker
pip install -r requirements.txt

**If you use allure:**
pytest -v --alluredir=allure_reports
allure serve .\allure_reports

**If you use only pytest:**
pytest -v

## Run with docker

### Create docker image
docker build .

### Run with docker
**If you use allure:**
docker run -t *container_id* pytest -v --alluredir=allure_reports
allure serve .\allure_reports

**If you use only pytest:**
docker run -t *container_id* pytest -v
