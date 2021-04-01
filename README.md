# Tests for restful-booker
[Restful booker](http://restful-booker.herokuapp.com/) is a public api.

I am learning pytest and how automate api. These tests are just my practice.

## Run without docker
pip install -r requirements.txt

**If you use allure:**<br>
```
pytest -v --alluredir=allure_reports
allure serve .\allure_reports
```

**If you use only pytest:**\
```pytest -v```

## Run with docker

### Create docker image
```docker build .```

**If you use allure:**
```
mkdir allure_results

docker run -v "$(pwd)"/allure_results:/usr/src/restful-booker/allure_results -t *container_id* pytest -v --alluredir=allure_results

allure serve .\allure_reports
```

**If you use only pytest:**<br>
```docker run -t *container_id* pytest -v```
