# selenium-search-tests

Sample project 

Install requirements:
```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt 
```

Run tests with Selenium Hub:
```
pytest tests/ --hub=localhost --remote=True
```

Run tests with local webdriver:
```
pytest tests/ --headless=True --browser=firefox --env=prod
```


Generate allure report:

```
pytest --alluredir ./alluredir

allure generate ./alluredir
```