import requests

def display(r):
    print((r.status_code, r.headers['Content-Type'], r.text))

print('key >>')
word=input()
key='?q='+word
addr='http://127.0.0.1:8000/'
url=addr + key


r=requests.get(url)
display(r)
assert r.status_code == 200