# core/services/bling.py
import requests

class BlingService:
    BASE_URL = "https://www.bling.com.br/Api/v3"

    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def buscar_produto_por_codigo(self, codigo: str) -> dict:
        url = f"{self.BASE_URL}/produtos"
        params = {"codigo": codigo}
        r = requests.get(url, headers=self.headers, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
