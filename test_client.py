import requests, zipfile, io

url = "http://localhost:8080/"


r = requests.get(url, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
print(z.extractall())
