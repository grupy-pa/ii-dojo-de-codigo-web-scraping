import os
import csv
import json
import requests
from bs4 import BeautifulSoup

def obter_html(url_ou_caminho: str) -> str:
    if url_ou_caminho.startswith("http://") or url_ou_caminho.startswith("https://"):
        response = requests.get(url_ou_caminho)
        response.raise_for_status()
        return response.text
    else:
        with open(url_ou_caminho, "r", encoding="utf-8") as f:
            return f.read()

def parsear_tabela(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    tabela = soup.find(id="tabela-estatisticas")
    if not tabela:
        # Tenta buscar por tag table genérica caso id não seja achado
        tabela = soup.find("table")
    
    dados = []
    if not tabela:
        return dados
        
    corpo = tabela.find("tbody")
    linhas = corpo.find_all("tr") if corpo else tabela.find_all("tr")[1:]
    
    for linha in linhas:
        colunas = linha.find_all("td")
        if not colunas or len(colunas) < 8:
            continue
            
        time = colunas[1].text.strip()
        jogos = int(colunas[2].text.strip())
        vitorias = int(colunas[3].text.strip())
        empates = int(colunas[4].text.strip())
        derrotas = int(colunas[5].text.strip())
        gols_pro = int(colunas[6].text.strip())
        gols_contra = int(colunas[7].text.strip())
        
        dados.append({
            "time": time,
            "jogos": jogos,
            "vitorias": vitorias,
            "empates": empates,
            "derrotas": derrotas,
            "gols_pro": gols_pro,
            "gols_contra": gols_contra
        })
        
    return dados

def calcular_metricas_e_ordenar(dados_brutos: list) -> list:
    dados_processados = []
    for time in dados_brutos:
        pontos = (time["vitorias"] * 3) + time["empates"]
        saldo_gols = time["gols_pro"] - time["gols_contra"]
        
        # Evita divisão por zero
        max_pontos = time["jogos"] * 3
        aproveitamento = round((pontos / max_pontos) * 100, 1) if max_pontos > 0 else 0.0
        
        # Copia dados e adiciona novos campos
        time_info = time.copy()
        time_info["pontos"] = pontos
        time_info["saldo_gols"] = saldo_gols
        time_info["aproveitamento"] = aproveitamento
        dados_processados.append(time_info)
        
    # Ordena: Pontos (decrescente) -> Saldo (decrescente) -> Vitórias (decrescente)
    dados_ordenados = sorted(
        dados_processados,
        key=lambda x: (x["pontos"], x["saldo_gols"], x["vitorias"]),
        reverse=True
    )
    
    # Atualiza a posição (Pos)
    for pos, time_info in enumerate(dados_ordenados, start=1):
        time_info["posicao"] = pos
        
    return dados_ordenados

def exportar_dados(dados: list, caminho_arquivo: str, formato: str = "json") -> None:
    if formato.lower() == "json":
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    elif formato.lower() == "csv":
        if not dados:
            return
        chaves = dados[0].keys()
        with open(caminho_arquivo, "w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=chaves)
            escritor.writeheader()
            escritor.writerows(dados)
    else:
        raise ValueError("Formato não suportado. Use 'json' ou 'csv'.")

if __name__ == "__main__":
    caminho_local = os.path.join("static", "parazao.html")
    print("Iniciando scraping da solução local...")
    try:
        html = obter_html(caminho_local)
        dados_brutos = parsear_tabela(html)
        dados_finais = calcular_metricas_e_ordenar(dados_brutos)
        
        exportar_dados(dados_finais, "classificacao_parazao.json", "json")
        exportar_dados(dados_finais, "classificacao_parazao.csv", "csv")
        
        print("Solução executada com sucesso! Resultados exportados.")
    except Exception as e:
        print(f"Erro na execução da solução: {e}")
