1. Ensure that you are in ```scrapper directory```.
2. Run ```python setup.py bdist_wheel```
3. Run ```docker-compose up```

Running Locally:

1. Install PostgresSQL on the machine
2. Run ```python setup.py bdist_wheel```
3. Run ```pip install -r requirements.txt```
4. Enter your DB credentials in ```session.py```.
5. Run ```python main.py```