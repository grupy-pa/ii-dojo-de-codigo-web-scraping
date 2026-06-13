import os
import csv
import json
import requests
from bs4 import BeautifulSoup

def obter_html(url_ou_caminho: str) -> str:
    """
    Round 1: Coleta de dados de páginas web
    Obtém o conteúdo HTML de uma URL (via requests) ou de um arquivo local.
    
    DICA: Se a string começar com 'http://' ou 'https://', use requests.get().
    Caso contrário, assuma que é um caminho de arquivo local e leia-o.
    """
    # TODO: Implementar a lógica de leitura/requisição
    raise NotImplementedError("Implementar no Round 1")

def parsear_tabela(html: str) -> list:
    """
    Round 2: Identificação de tabelas e informações úteis
    Round 3: Limpeza e organização dos dados
    
    Recebe o HTML cru, localiza a tabela '#tabela-estatisticas',
    e extrai os dados brutos de cada time.
    
    Retorna uma lista de dicionários contendo os dados limpos (com tipos corretos):
    [
        {
            "time": "Paysandu",
            "jogos": 10,
            "vitorias": 7,
            "empates": 2,
            "derrotas": 1,
            "gols_pro": 18,
            "gols_contra": 5
        },
        ...
    ]
    """
    # TODO: Usar BeautifulSoup para navegar pelas linhas (tr) da tabela e extrair os dados.
    # Certifique-se de limpar espaços em branco com .strip() e converter números para int.
    raise NotImplementedError("Implementar nos Rounds 2 e 3")

def calcular_metricas_e_ordenar(dados_brutos: list) -> list:
    """
    Round 4: Cálculo de métricas (pontos, saldo de gols e aproveitamento)
    Recebe a lista de dados brutos e para cada time calcula:
    - pontos: (vitorias * 3) + empates
    - saldo_gols: gols_pro - gols_contra
    - aproveitamento: (pontos / (jogos * 3)) * 100 (arredondado para 1 casa decimal)
    
    Em seguida, ordena a lista com base nos critérios de desempate:
    1. Pontos (decrescente)
    2. Saldo de Gols (decrescente)
    3. Vitórias (decrescente)
    
    Retorna a lista ordenada com os novos campos.
    """
    # TODO: Implementar cálculos das métricas e ordenação final da tabela.
    raise NotImplementedError("Implementar no Round 4")

def exportar_dados(dados: list, caminho_arquivo: str, formato: str = "json") -> None:
    """
    Round 5: Exportação dos dados em CSV ou JSON
    Salva os dados finais em um arquivo JSON ou CSV, dependendo do formato solicitado.
    Assegure-se de que a codificação seja UTF-8.
    """
    # TODO: Implementar exportação para JSON ou CSV
    raise NotImplementedError("Implementar no Round 5")

if __name__ == "__main__":
    # Script principal para execução manual
    caminho_local = os.path.join("static", "parazao.html")
    print("Iniciando scraping local...")
    try:
        html = obter_html(caminho_local)
        dados_brutos = parsear_tabela(html)
        dados_finais = calcular_metricas_e_ordenar(dados_brutos)
        
        # Testar exportações
        exportar_dados(dados_finais, "classificacao_parazao.json", "json")
        exportar_dados(dados_finais, "classificacao_parazao.csv", "csv")
        
        print("Scraping concluído e arquivos exportados com sucesso!")
    except Exception as e:
        print(f"Erro na execução: {e}")
