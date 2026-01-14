# avi/core/services/anymarket.py

import requests
token = "MjU5MDYzNTc1Lg==.MUfqIGh9hJCl8gZ0ji+YXHX7aX1SucmOJntr/d0/QjNRjd8WVDk1nXie3s2dX4yf99em09OD7rCS1OYo8Ek+Mw=="

def consumir_skus_anymarket(token):
    url = "https://api.anymarket.com.br/v2/skus"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def atualizar_sku_anymarket(sku_id, dados, token):
    url = f"https://api.anymarket.com.br/v2/skus/{sku_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, json=dados)
    response.raise_for_status()
    return response.json()
