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
                    dados_limpos.append({
                        "ano": int(ano),
                        "fase": celulas[1].strip(),
                        "posicao": celulas[2].strip(),
                        "jogos": int(jogos),
                        "vitorias": int(celulas[4].strip()),
                        "empates": int(celulas[5].split("[")[0].strip()), # Limpa notas no E[i]
                        "derrotas": int(celulas[6].strip()),
                        "gols_pro": int(celulas[7].strip()),
                        "gols_contra": int(celulas[8].strip())
                    })

print(f"Total de registros coletados: {len(dados_limpos)}")
if dados_limpos:
    print("\nRegistros coletados por ano:")
    for registro in dados_limpos:
        print(f"Copa de {registro['ano']}: {registro}")

