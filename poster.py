import requests

url = "http://localhost:5000/post/testing"

obj = {"name":"Lenard","age":"5"}

x = requests.post(url,json=obj)

print(x.text)

