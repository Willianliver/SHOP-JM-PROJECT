from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
import os
from rest_framework import status
from .models import LogBusca
from . import logic
import requests

ARQUIVO = r'C:\Users\pires\Desktop\SHOP JM PROJECT\avi\core\planilhas\SKUxCANAL_Release_ATT.csv'
TOKEN_MATRIZ = 'MjU5MDI2OTI0Lg==.Aqjrl2pPs+LCjB3E23tkmD+uqwdiwk9lGvgOuT52ZtlghRItHsj1X6RD8lJzRVQHX0JpKWlVs7e/zHl5OES0Jg=='
TOKEN_FILIAL = '259037346L1E1706474176096C161316217609600O1'

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
    

def matriz(request):
    mensagem = ""

    if request.method == 'POST':
        sku = request.POST.get('sku')
        id_prod_hub = request.POST.get('id_prod_hub')

        token = 'MjU5MDI2OTI0Lg==.Aqjrl2pPs+LCjB3E23tkmD+uqwdiwk9lGvgOuT52ZtlghRItHsj1X6RD8lJzRVQHX0JpKWlVs7e/zHl5OES0Jg=='
        arquivo = r'C:\Users\pires\Desktop\SHOP JM PROJECT\avi\core\planilhas\SKUxCANAL_Release_ATT.csv'

        url = f"http://api.anymarket.com.br/v2/products/{id_prod_hub}"
        headers = {"Content-Type": "application/json", "gumgaToken": token}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            sku_hub = data.get("skus", [{}])[0].get("id")

            if sku_hub:
                try:
                    df = pd.read_csv(arquivo, sep=";", encoding="latin1", header=None, dtype=str)
                except FileNotFoundError:
                    df = pd.DataFrame()

                inicio = encontrar_bloco_vazio(df)

                fim = inicio + 25
                while len(df) <= fim:
                    df.loc[len(df)] = [""] * max(7, len(df.columns))

                valores_coluna_a = df.iloc[3:30, 0].tolist() if len(df) >= 30 else [""] * 27
                valores_coluna_e = df.iloc[3:30, 4].tolist() if len(df) >= 30 else [""] * 27
                valores_coluna_f = df.iloc[3:30, 5].tolist() if len(df) >= 30 else [""] * 27
                valores_coluna_g = df.iloc[3:30, 6].tolist() if len(df) >= 30 else [""] * 27

                for i in range(inicio, fim + 1):
                    df.loc[i, 0] = valores_coluna_a[i - inicio]
                    df.loc[i, 4] = valores_coluna_e[i - inicio]
                    df.loc[i, 5] = valores_coluna_f[i - inicio]
                    df.loc[i, 6] = valores_coluna_g[i - inicio]

                for i in range(inicio, inicio + 20):
                    df.loc[i, 1] = sku
                    df.loc[i, 2] = id_prod_hub
                    df.loc[i, 3] = sku_hub

                df.to_csv(arquivo, sep=";", index=False, encoding="latin1", header=False)
                mensagem = f"✅ SKU {sku} (MATRIZ) atualizado com sucesso!"
            else:
                mensagem = "❌ Erro: ID do SKU não encontrado na resposta da API."
        else:
            mensagem = f"❌ Erro na requisição: {response.status_code} - {response.text}"

    return render(request, 'avi/form.html', {'mensagem': mensagem, 'aba': 'matriz'})

def encontrar_bloco_vazio(df):
    bloco_tamanho = 26
    linha_inicial = 3

    while True:
        bloco = df.iloc[linha_inicial:linha_inicial + bloco_tamanho] if linha_inicial + bloco_tamanho <= len(df) else pd.DataFrame()

        if bloco.empty or bloco[[1, 2, 3]].isnull().all().all() or (bloco[[1, 2, 3]] == "").all().all():
            return linha_inicial

        linha_inicial += bloco_tamanho
        if linha_inicial >= len(df):
            return linha_inicial
        
def filial(request):
    mensagem = ""

    if request.method == 'POST':
        sku = request.POST.get('sku')
        id_prod_hub = request.POST.get('id_prod_hub')

        token = '259037346L1E1706474176096C161316217609600O1'
        arquivo = r'C:\Users\pires\Desktop\SHOP JM PROJECT\avi\core\planilhas\SKUxCANAL_Release_ATT.csv'

        url = f"http://api.anymarket.com.br/v2/products/{id_prod_hub}"
        headers = {"Content-Type": "application/json", "gumgaToken": token}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            sku_hub = data.get("skus", [{}])[0].get("id")

            if sku_hub:
                try:
                    df = pd.read_csv(arquivo, sep=";", encoding="latin1", header=None, dtype=str)
                except FileNotFoundError:
                    df = pd.DataFrame()

                inicio = encontrar_proxima_linha(df)

                while len(df) <= inicio + 4:
                    df.loc[len(df)] = [""] * max(7, len(df.columns))

                for i in range(inicio, inicio + 6):
                    df.loc[i, 1] = sku
                    df.loc[i, 2] = id_prod_hub
                    df.loc[i, 3] = sku_hub

                df.to_csv(arquivo, sep=";", index=False, encoding="latin1", header=False)
                mensagem = f"✅ SKU {sku} (FILIAL) atualizado com sucesso!"
            else:
                mensagem = "❌ Erro: ID do SKU não encontrado na resposta da API."
        else:
            mensagem = f"❌ Erro na requisição: {response.status_code} - {response.text}"

    return render(request, 'avi/form.html', {'mensagem': mensagem, 'aba': 'filial'})

def encontrar_proxima_linha(df):
    linhas_ocupadas = df[df[0].notnull()].index.tolist()

    if not linhas_ocupadas:
        return 23  # Começa na linha 24 (índice 23)

    ultima_linha = max(linhas_ocupadas)
    proxima_linha = ultima_linha + 1

    if (proxima_linha - 23) % 26 != 0:
        proxima_linha = 23 + (((proxima_linha - 23) // 26) + 1) * 26

    return proxima_linha

def download_planilha(request):
    filepath = os.path.join(os.path.dirname(__file__), r'C:\Users\pires\Desktop\SHOP JM PROJECT\avi\core\planilhas\SKUxCANAL_Release_ATT.csv')

    try:
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='SKUxCANAL_Release_ATT.csv')
    except FileNotFoundError:
        return render(request, 'form.html', {'mensagem': '❌ Arquivo não encontrado.', 'aba': 'matriz'})