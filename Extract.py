import requests


url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00240/UCI%20HAR%20Dataset.zip"

r = requests.get(url, allow_redirects=True)
open('dataset.zip', 'wb').write(r.content)