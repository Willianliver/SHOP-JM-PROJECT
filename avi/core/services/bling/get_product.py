import requests

url = "https://api.bling.com.br/Api/v3/produtos/variacoes/16590452290"

payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer 4ed1db11d6080629d95995b83775c5a300b84093',
  'Cookie': 'PHPSESSID=iu5dqe6h5ib3m1b6ogevt0uknf'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
