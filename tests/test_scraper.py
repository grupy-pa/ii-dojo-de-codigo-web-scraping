import os
import pytest
from src.scraper import obter_html, parsear_tabela, calcular_metricas_e_ordenar, exportar_dados

# Mock simples do HTML para os testes
HTML_MOCK = """
<table>
    <table id="tabela-estatisticas">
        <thead>
            <tr>
                <th>Pos</th>
                <th>Time</th>
                <th>J</th>
                <th>V</th>
                <th>E</th>
                <th>D</th>
                <th>GP</th>
                <th>GC</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>-</td>
                <td> Paysandu </td>
                <td>10</td>
                <td>7</td>
                <td>2</td>
                <td>1</td>
                <td>18</td>
                <td>5</td>
            </tr>
            <tr>
                <td>-</td>
                <td> Remo </td>
                <td>10</td>
                <td>6</td>
                <td>2</td>
                <td>2</td>
                <td>15</td>
                <td>7</td>
            </tr>
        </tbody>
    </table>
</table>
"""

def test_obter_html_local():
    # Testa a leitura local usando o arquivo static/parazao.html
    caminho = os.path.join("static", "parazao.html")
    html = obter_html(caminho)
    assert "<title>Campeonato Paraense - Tabela de Classificação</title>" in html
    assert "id=\"tabela-estatisticas\"" in html

def test_parsear_tabela():
    # Testa se o parser extrai as linhas e converte os tipos corretamente
    dados = parsear_tabela(HTML_MOCK)
    assert len(dados) == 2
    assert dados[0]["time"] == "Paysandu"
    assert dados[0]["jogos"] == 10
    assert dados[0]["vitorias"] == 7
    assert dados[0]["empates"] == 2
    assert dados[0]["derrotas"] == 1
    assert dados[0]["gols_pro"] == 18
    assert dados[0]["gols_contra"] == 5

def test_calcular_metricas_e_ordenar():
    # Testa cálculos e ordenação corretos
    dados_brutos = [
        {
            "time": "Remo",
            "jogos": 10,
            "vitorias": 6,
            "empates": 2,
            "derrotas": 2,
            "gols_pro": 15,
            "gols_contra": 7
        },
        {
            "time": "Paysandu",
            "jogos": 10,
            "vitorias": 7,
            "empates": 2,
            "derrotas": 1,
            "gols_pro": 18,
            "gols_contra": 5
        }
    ]
    
    dados_finais = calcular_metricas_e_ordenar(dados_brutos)
    
    # Paysandu deve ser o 1º devido ao maior número de pontos (23 vs 20)
    assert dados_finais[0]["time"] == "Paysandu"
    assert dados_finais[0]["pontos"] == 23
    assert dados_finais[0]["saldo_gols"] == 13
    assert dados_finais[0]["aproveitamento"] == 76.7 # (23 / 30) * 100
    
    # Remo deve ser o 2º
    assert dados_finais[1]["time"] == "Remo"
    assert dados_finais[1]["pontos"] == 20
    assert dados_finais[1]["saldo_gols"] == 8
    assert dados_finais[1]["aproveitamento"] == 66.7 # (20 / 30) * 100

def test_exportar_dados_json(tmp_path):
    dados = [
        {
            "time": "Paysandu",
            "jogos": 10,
            "pontos": 23,
            "saldo_gols": 13,
            "aproveitamento": 76.7
        }
    ]
    caminho = tmp_path / "test.json"
    exportar_dados(dados, str(caminho), "json")
    
    assert caminho.exists()
    import json
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = json.load(f)
        assert conteudo[0]["time"] == "Paysandu"

def test_exportar_dados_csv(tmp_path):
    dados = [
        {
            "time": "Paysandu",
            "jogos": 10,
            "pontos": 23,
            "saldo_gols": 13,
            "aproveitamento": 76.7
        }
    ]
    caminho = tmp_path / "test.csv"
    exportar_dados(dados, str(caminho), "csv")
    
    assert caminho.exists()
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = f.read().splitlines()
        assert "time,jogos,pontos,saldo_gols,aproveitamento" in linhas[0]
        assert "Paysandu,10,23,13,76.7" in linhas[1]
