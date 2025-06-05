from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LogBusca
import requests


def buscar_produto_anymarket(request, id_produto):
    url = f'https://api.anymarket.com.br/v2/products/{id_produto}'

    headers = {
        'Content-Type': 'application/json',
        'gumgaToken': 'MjU5MDI2OTI0Lg==.Aqjrl2pPs+LCjB3E23tkmD+uqwdiwk9lGvgOuT52ZtlghRItHsj1X6RD8lJzRVQHX0JpKWlVs7e/zHl5OES0Jg=='
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()

            # Pega a primeira SKU e imagem como principais
            sku_data = data.get('skus', [{}])[0]
            imagem_principal = next((img.get('url') for img in data.get('images', []) if img.get('main')), None)

            contexto = {
                'id': data.get('id'),
                'titulo': data.get('title'),
                'descricao': data.get('description'),
                'categoria': data.get('category', {}).get('name'),
                'marca': data.get('brand', {}).get('name'),
                'modelo': data.get('model'),
                'genero': data.get('gender'),
                'garantia': data.get('warrantyText'),
                'peso': data.get('weight'),
                'largura': data.get('width'),
                'altura': data.get('height'),
                'comprimento': data.get('length'),
                'sku': sku_data.get('partnerId'),
                'ean': sku_data.get('ean'),
                'preco': sku_data.get('sellPrice'),
                'estoque': sku_data.get('amount'),
                'imagem': imagem_principal,
                'caracteristicas': data.get('characteristics', []),
                'ativo': data.get('isProductActive'),
            }

            return render(request, 'avi/produtos.html',  contexto)

        return render(request, 'avi/produtos.html', {
            'erro': f'Erro na requisição. Status {response.status_code}',
            'detalhe': response.text
        })

    except Exception as e:
        return render(request, 'avi/produtos.html', {
            'erro': 'Erro ao fazer a requisição.',
            'detalhe': str(e)
        })