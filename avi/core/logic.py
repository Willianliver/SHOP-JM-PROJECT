import requests
import pandas as pd


def buscar_ids(sku, id_prod_hub, token):
    url = f"https://api.anymarket.com.br/v2/products/{id_prod_hub}"
    headers = {"Content-Type": "application/json", "gumgaToken": token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        sku_hub = data.get("skus", [{}])[0].get("id")

        if sku_hub is not None:
            return sku, id_prod_hub, int(sku_hub)
        else:
            raise Exception("❌ ID do SKU não encontrado na resposta da API.")
    else:
        raise Exception(f"❌ Erro ao buscar SKU {sku}: {response.status_code} - {response.text}")


def encontrar_bloco_vazio(arquivo):
    try:
        df = pd.read_csv(arquivo, sep=";", encoding="latin1", header=None, dtype=str)
    except FileNotFoundError:
        return 3

    bloco_tamanho = 26
    linha_inicial = 3

    while True:
        bloco = df.iloc[linha_inicial:linha_inicial + bloco_tamanho]
        colunas_verificar = bloco[[1, 2, 3]]
        if colunas_verificar.isnull().all().all() or (colunas_verificar == "").all().all():
            return linha_inicial

        linha_inicial += bloco_tamanho
        if linha_inicial >= len(df):
            return linha_inicial


def atualizar_planilha(arquivo, sku, id_prod_hub, sku_hub, inicio):
    try:
        df = pd.read_csv(arquivo, sep=";", encoding="latin1", header=None, dtype=str)
    except FileNotFoundError:
        df = pd.DataFrame()

    fim = inicio + 25

    while len(df) <= fim:
        df.loc[len(df)] = [""] * max(7, df.shape[1] if not df.empty else 7)

    valores_coluna_a = df.iloc[3:30, 0].tolist()
    valores_coluna_e = df.iloc[3:30, 4].tolist()
    valores_coluna_f = df.iloc[3:30, 5].tolist()
    valores_coluna_g = df.iloc[3:30, 6].tolist()

    for i in range(inicio, fim + 1):
        df.loc[i, 0] = valores_coluna_a[i - inicio] if i - inicio < len(valores_coluna_a) else ""
        df.loc[i, 4] = valores_coluna_e[i - inicio] if i - inicio < len(valores_coluna_e) else ""
        df.loc[i, 5] = valores_coluna_f[i - inicio] if i - inicio < len(valores_coluna_f) else ""
        df.loc[i, 6] = valores_coluna_g[i - inicio] if i - inicio < len(valores_coluna_g) else ""

    for i in range(inicio, inicio + 20):
        df.loc[i, 1] = sku
        df.loc[i, 2] = id_prod_hub
        df.loc[i, 3] = sku_hub

    df.to_csv(arquivo, sep=";", index=False, encoding="latin1", header=False)

    return f"✅ SKU {sku} atualizado nas linhas {inicio + 1} a {fim + 1}."
