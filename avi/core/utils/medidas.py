# avi/utils/medidas.py

def calcular_cubagem(altura_cm, largura_cm, comprimento_cm):
    try:
        return (altura_cm * largura_cm * comprimento_cm) * 300
    except TypeError:
        return 0  # ou None, dependendo de como você quiser tratar erros
    
# avi/core/utils/medidas.py

def to_cm(valor, unidade: str):
    if valor is None:
        return None
    unidade = (unidade or "").lower()
    if unidade in ("cm", ""):
        return float(valor)
    if unidade == "mm":
        return float(valor) / 10
    if unidade == "m":
        return float(valor) * 100
    raise ValueError(f"Unidade de medida desconhecida: {unidade}")

def to_kg(valor, unidade: str):
    if valor is None:
        return None
    unidade = (unidade or "").lower()
    if unidade in ("kg", ""):
        return float(valor)
    if unidade == "g":
        return float(valor) / 1000
    raise ValueError(f"Unidade de peso desconhecida: {unidade}")

def peso_cubado_kg(altura_cm, largura_cm, comprimento_cm, fator=250):
    # fator comum: 250 kg/m³ ou 300 kg/m³ (você define)
    volume_m3 = (altura_cm/100) * (largura_cm/100) * (comprimento_cm/100)
    return round(volume_m3 * fator, 3)

def peso_final_kg(peso_real_kg, peso_cubado_kg_):
    return max(peso_real_kg, peso_cubado_kg_)
