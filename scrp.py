import csv
import requests
from bs4 import BeautifulSoup

# A Wikipédia não bloqueia requisições se passarmos um User-Agent descritivo
url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"

headers = {
    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11",
    "Accept": "*/*"
}

resp = requests.get(url, headers=headers)
print("Status Code:", resp.status_code)

dados_limpos = []

if resp.status_code == 200:
    soup = BeautifulSoup(resp.text, "html.parser")
    # A tabela com o desempenho histórico do Brasil possui a classe 'wikitable'
    table = soup.find("table", class_="wikitable")
    
    if table:
        rows = table.find_all("tr")
        for row in rows:
            # Extrai o texto de todas as células (td ou th) limpando espaços em branco
            celulas = [celula.get_text(strip=True) for celula in row.find_all(["td", "th"])]
            
            # Filtra apenas as linhas com o número correto de colunas (Ano, Fase, Posição, J, V, E, D, GP, GC)
            if len(celulas) >= 9:
                ano = celulas[0].split("[")[0].strip() # Limpa notas de rodapé como 1950[ii]
                jogos = celulas[3].strip()
                
                # Ignora o cabeçalho ("Ano"), a linha de "Total" e anos futuros "A definir" (que não têm número de jogos)
                if ano != "Ano" and "Total" not in ano and jogos.isdigit():
                    vitorias = int(celulas[4].strip())
                    empates = int(celulas[5].split("[")[0].strip())
                    derrotas = int(celulas[6].strip())
                    gols_pro = int(celulas[7].strip())
                    gols_contra = int(celulas[8].strip())
                    
                    # Cálculo das métricas (conforme definido no README)
                    pontos = (vitorias * 3) + empates
                    saldo_gols = gols_pro - gols_contra
                    aproveitamento = round((pontos / (int(jogos) * 3)) * 100, 2) if int(jogos) > 0 else 0.0

                    dados_limpos.append({
                        "ano": int(ano),
                        "fase": celulas[1].strip(),
                        "posicao": celulas[2].strip(),
                        "jogos": int(jogos),
                        "vitorias": vitorias,
                        "empates": empates,
                        "derrotas": derrotas,
                        "gols_pro": gols_pro,
                        "gols_contra": gols_contra,
                        "pontos": pontos,
                        "saldo_gols": saldo_gols,
                        "aproveitamento": aproveitamento
                    })

print(f"Total de registros coletados: {len(dados_limpos)}")
if dados_limpos:
    print("\nRegistros coletados por ano:")
    for registro in dados_limpos:
        print(f"Copa de {registro['ano']}: {registro}")

    # Salva os dados em formato CSV
    with open("brasil_copas.csv", mode="w", encoding="utf-8", newline="") as f:
        campos = [
            "ano", "fase", "posicao", "jogos", "vitorias", "empates", "derrotas", 
            "gols_pro", "gols_contra", "pontos", "saldo_gols", "aproveitamento"
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados_limpos)
    
    print("\nDados salvos com sucesso em 'brasil_copas.csv'!")

    # --- ANÁLISE COM PANDAS E NUMPY ---
    print("\n" + "="*40)
    print("      ANÁLISE COM PANDAS E NUMPY")
    print("="*40)
    import pandas as pd
    import numpy as np

    df = pd.read_csv("brasil_copas.csv")

    # 1. Eficiência Ofensiva e Defensiva Média
    total_jogos = df["jogos"].sum()
    efic_ofensiva = df["gols_pro"].sum() / total_jogos
    efic_defensiva = df["gols_contra"].sum() / total_jogos

    print(f"⚽ Eficiência Ofensiva Média: {efic_ofensiva:.2f} gols marcados por jogo")
    print(f"🛡️ Eficiência Defensiva Média: {efic_defensiva:.2f} gols sofridos por jogo")

    # 2. Consistência de Desempenho (Desvio Padrão)
    std_aproveitamento = np.std(df["aproveitamento"])
    std_saldo = np.std(df["saldo_gols"])

    print(f"📊 Desvio Padrão do Aproveitamento: {std_aproveitamento:.2f}%")
    print(f"📊 Desvio Padrão do Saldo de Gols: {std_saldo:.2f}")

    # 3. Modelo Matemático para Chances do Hexa
    # Considera o aproveitamento histórico (peso 30%), o aproveitamento recente das últimas 5 Copas (peso 40%)
    # e a proporção de gols marcados/sofridos histórica (peso 30%)
    aproveitamento_historico = df["aproveitamento"].mean() / 100
    aproveitamento_recente = df.tail(5)["aproveitamento"].mean() / 100
    proporcao_gols = df["gols_pro"].sum() / df["gols_contra"].sum()
    
    # Normalizamos a proporção de gols dividindo por 3 (um valor máximo de referência de dominância)
    eficiencia_gols = min(proporcao_gols / 3, 1.0)

    probabilidade_hexa = (0.3 * aproveitamento_historico) + (0.4 * aproveitamento_recente) + (0.3 * eficiencia_gols)
    probabilidade_hexa_percentual = min(probabilidade_hexa * 100, 100.0)

    print("\n" + "="*40)
    print("  MODELO MATEMÁTICO: CHANCES DO HEXA 🌟")
    print("="*40)
    print(f"📈 Aproveitamento Histórico Médio: {aproveitamento_historico * 100:.2f}%")
    print(f"📈 Aproveitamento Recente Médio (Últimas 5 Copas): {aproveitamento_recente * 100:.2f}%")
    print(f"⚔️  Razão de Gols Histórica (Pró/Contra): {proporcao_gols:.2f}")
    print(f"🏆 Chances Calculadas do Brasil ganhar o Hexa: {probabilidade_hexa_percentual:.2f}%")
    print("="*40)


