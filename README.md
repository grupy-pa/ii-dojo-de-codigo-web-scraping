# II Dojo de Código: Web Scraping com Python - GruPy Pará

## ⚽ Desempenho do Brasil nas últimas Copas do Mundo

**Horário:** 09:00 às 11:30

---

## 🥋 O que é um Dojo de Código (Coding Dojo)?

O **Coding Dojo** é um encontro de programação onde os participantes se reúnem para praticar e aprender de forma colaborativa. O foco não é apenas concluir o desafio ou criar o código mais rápido, mas sim **aprimorar habilidades**, debater boas práticas de desenvolvimento, trabalhar em equipe e aprender coletivamente em um ambiente seguro de experimentação.

Nessa dinâmica:
- **Programação em Par (Pair Programming)**: Os participantes se revezam no desenvolvimento da solução.
- **Iterativo e Incremental**: Dividimos o problema maior em passos menores e mais simples.
- **Aprendizado Coletivo**: Todos contribuem com ideias, tiram dúvidas e compartilham experiências.

---

## 📋 Atividades Realizadas

Durante o dojo, passaremos pelas seguintes etapas estruturadas:

1. **Pesquisa e Inspeção (Rounds 1 e 2)**: Identificar e inspecionar fontes de dados válidas usando ferramentas de desenvolvedor do navegador (F12) para encontrar tabelas de interesse.
2. **Primeiros Acessos com Python (Round 3)**: Efetuar requisições HTTP e configurar o cabeçalho `User-Agent` para obter o conteúdo das páginas.
3. **Parse de HTML (Round 4)**: Carregar a estrutura de tags no BeautifulSoup e navegar pelas tabelas da página.
4. **Extração de Dados (Round 5)**: Ler e mapear as linhas e células desejadas.
5. **Limpeza e Tratamento de Dados (Round 6)**: Limpar textos, remover caracteres e notas de rodapé, tratar dados ausentes e converter tipos numéricos.
6. **Cálculo de Métricas e Exportação (Round 7)**: Implementar fórmulas matemáticas simples (como saldo de gols e aproveitamento) e salvar os dados consolidados em formato CSV.
7. **Análise Estatística e Preditiva com Pandas e NumPy (Bônus)**: Ler os dados salvos em CSV para calcular a eficiência de gols, o desvio padrão de desempenho e aplicar um modelo de probabilidade para estimar as chances de conquistar o Hexa.
8. **Retrospectiva**: Discutir o que aprendemos, o que facilitou/dificultou a dinâmica e propor melhorias para próximas edições.

---

## 📚 Tópicos Abordados

No decorrer das atividades, serão estudados e praticados os seguintes assuntos:

- **Conceitos de Web Scraping e Web**:
  - Funcionamento de requisições HTTP (verbos HTTP, headers, status codes).
  - Configuração de `User-Agent` para identificação de scripts.
  - Estruturação de documentos HTML, tags (`table`, `tr`, `td`, `th`) e atributos CSS.
- **Linguagem Python**:
  - Manipulação, limpeza e fatiamento de strings (`strip()`, `split()`, concatenação).
  - Estruturas de dados essenciais (`list`, `dict`, `range`).
  - Estruturas de repetição (loops com `for`) e desvios condicionais (`if/else`).
  - Conversões de tipos de dados (casting para `int`, etc.).
  - Tratamento de exceções e erros (`try/except`).
- **Bibliotecas Principais**:
  - `requests`: para consumo de dados via HTTP.
  - `BeautifulSoup` (da biblioteca `beautifulsoup4`): para parseamento e extração de dados HTML.
  - `pandas` e `numpy`: para manipulação de DataFrames, estatística básica e cálculos vetoriais.
- **Engenharia e Qualidade de Software**:
  - Programação pareada e rotação de participantes.
  - Refatoração contínua de código para legibilidade.
  - Persistência e estruturação de arquivos CSV.

---

## Fonte sugerida

A fonte principal sugerida para o dojo é a Wikipédia em português:

```text
https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA
```

A página possui informações organizadas em tabelas, o que facilita o estudo inicial de web scraping.

---

## Sequência de Desenvolvimento (Passo a Passo)

Abaixo está a sequência detalhada que seguiremos para construir o scraper da Wikipédia, mostrando o código resultante e o **diff** (linhas com `+` indicam o que adicionar, e `-` o que remover) para orientar o aluno em cada passo.

---

### 1 - conectar ao site
Criamos a primeira versão do script para simplesmente disparar uma requisição HTTP.

**Código resultante:**
```python
import requests

url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
resp = requests.get(url)
print(resp.status_code)
```

---

### 2 - fazer a requisição com o user-agent
Muitas páginas retornam erros ou bloqueiam requisições genéricas (como o cabeçalho padrão da biblioteca python-requests). Contornamos isso adicionando um `User-Agent`.

**Diff em relação ao passo anterior:**
```diff
 import requests
 
 url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
-resp = requests.get(url)
+headers = {
+    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
+}
+resp = requests.get(url, headers=headers)
 print(resp.status_code)
```

**Código resultante:**
```python
import requests

url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
headers = {
    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
}
resp = requests.get(url, headers=headers)
print(resp.status_code)
```

---

### 3 - testar uma sequencia de requisições - spider
Para compreender como percorrer várias páginas (como se estivéssemos raspando dados sequenciais), podemos testar um loop sobre as edições de Copa do Mundo.

**Diff em relação ao passo anterior:**
```diff
 import requests
 
-url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
 headers = {
     "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
 }
-resp = requests.get(url, headers=headers)
-print(resp.status_code)
+
+for ano in range(1970, 2023, 4):
+    url = f"https://pt.wikipedia.org/wiki/Copa_do_Mundo_FIFA_de_{ano}"
+    resp = requests.get(url, headers=headers)
+    print(resp.status_code, ano)
```

**Código resultante:**
```python
import requests

headers = {
    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
}

for ano in range(1970, 2023, 4):
    url = f"https://pt.wikipedia.org/wiki/Copa_do_Mundo_FIFA_de_{ano}"
    resp = requests.get(url, headers=headers)
    print(resp.status_code, ano)
```

---

### 4 - carregar o html de cada página e analisar com BeautifulSoup
Carregamos o corpo do HTML usando a biblioteca BeautifulSoup de forma que possamos analisá-lo e imprimi-lo de forma legível (prettify).

**Diff em relação ao passo anterior:**
```diff
 import requests
+from bs4 import BeautifulSoup
 
 headers = {
     "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
 }
 
 for ano in range(1970, 2023, 4):
     url = f"https://pt.wikipedia.org/wiki/Copa_do_Mundo_FIFA_de_{ano}"
     resp = requests.get(url, headers=headers)
-    print(resp.status_code, ano)
+    soup = BeautifulSoup(resp.text, "html.parser")
+    print(soup.prettify()[:1000])
```

**Código resultante:**
```python
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
}

for ano in range(1970, 2023, 4):
    url = f"https://pt.wikipedia.org/wiki/Copa_do_Mundo_FIFA_de_{ano}"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    print(soup.prettify()[:1000])
```

---

### 5 - Analisar o layout da página e inspecionar os elementos com Browser (F12) para identificar padrões na estrutura HTML
Utilizando a ferramenta Inspecionar (F12) no navegador, navegamos até a tabela principal de participações na página consolidada `Brasil na Copa do Mundo FIFA`. Vemos que a tabela possui a classe CSS `wikitable` e cada linha da tabela é definida por `<tr>` com células em `<th>` (cabeçalho) ou `<td>` (dados).

---

### 6 - filtrar tabelas com BeautifulSoup
Como faremos a extração a partir da tabela histórica consolidada, voltamos a nossa requisição para a página principal do Brasil e filtramos apenas a tabela que possui a classe `wikitable`.

**Diff em relação ao passo anterior:**
```diff
 import requests
 from bs4 import BeautifulSoup
 
+url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
 headers = {
     "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
 }
 
-for ano in range(1970, 2023, 4):
-    url = f"https://pt.wikipedia.org/wiki/Copa_do_Mundo_FIFA_de_{ano}"
-    resp = requests.get(url, headers=headers)
-    soup = BeautifulSoup(resp.text, "html.parser")
-    print(soup.prettify()[:1000])
+resp = requests.get(url, headers=headers)
+soup = BeautifulSoup(resp.text, "html.parser")
+table = soup.find("table", class_="wikitable")
+print(table.prettify()[:1000])
```

**Código resultante:**
```python
import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
headers = {
    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", class_="wikitable")
print(table.prettify()[:1000])
```

---

### 7 - extraindo as linhas das tabelas (rows)
A partir da tabela identificada, extraímos todas as linhas (`<tr>`).

**Diff em relação ao passo anterior:**
```diff
 resp = requests.get(url, headers=headers)
 soup = BeautifulSoup(resp.text, "html.parser")
 table = soup.find("table", class_="wikitable")
-print(table.prettify()[:1000])
+rows = table.find_all("tr")
+print(rows[:3])
```

**Código resultante:**
```python
import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
headers = {
    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", class_="wikitable")
rows = table.find_all("tr")
print(rows[:3])
```

---

### 8 - efetuando uma limpeza nos dados coletados e armazenando dados mais limpos
Limpamos as quebras de linha e referências/notas de rodapé de texto da Wikipédia (ex: `1950[ii]` vira `1950` e `E[i]` vira `E`), descartamos as linhas inúteis da tabela (como cabeçalhos redundantes, anos futuros a definir e a linha total de sumário) e montamos nossa lista de dicionários limpos convertendo os valores numéricos para inteiros.

**Diff em relação ao passo anterior:**
```diff
 resp = requests.get(url, headers=headers)
 soup = BeautifulSoup(resp.text, "html.parser")
 table = soup.find("table", class_="wikitable")
 rows = table.find_all("tr")
-print(rows[:3])
+
+dados_limpos = []
+
+for row in rows:
+    # Extrai o texto de todas as células da linha
+    celulas = [celula.get_text(strip=True) for celula in row.find_all(["td", "th"])]
+    
+    # Filtra apenas linhas com dados válidos da tabela
+    if len(celulas) >= 9:
+        ano = celulas[0].split("[")[0].strip() # Limpa notas de rodapé como 1950[ii]
+        jogos = celulas[3].strip()
+        
+        # Ignora cabeçalhos, totais e edições futuras
+        if ano != "Ano" and "Total" not in ano and jogos.isdigit():
+            dados_limpos.append({
+                "ano": int(ano),
+                "fase": celulas[1].strip(),
+                "posicao": celulas[2].strip(),
+                "jogos": int(jogos),
+                "vitorias": int(celulas[4].strip()),
+                "empates": int(celulas[5].split("[")[0].strip()), # Limpa E[i]
+                "derrotas": int(celulas[6].strip()),
+                "gols_pro": int(celulas[7].strip()),
+                "gols_contra": int(celulas[8].strip())
+            })
+
+print(dados_limpos)
```

**Código resultante:**
```python
import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
headers = {
    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", class_="wikitable")
rows = table.find_all("tr")

dados_limpos = []

for row in rows:
    celulas = [celula.get_text(strip=True) for celula in row.find_all(["td", "th"])]
    if len(celulas) >= 9:
        ano = celulas[0].split("[")[0].strip() # Limpa notas de rodapé como 1950[ii]
        jogos = celulas[3].strip()
        
        # Ignora cabeçalhos, totais e edições futuras "A definir"
        if ano != "Ano" and "Total" not in ano and jogos.isdigit():
            dados_limpos.append({
                "ano": int(ano),
                "fase": celulas[1].strip(),
                "posicao": celulas[2].strip(),
                "jogos": int(jogos),
                "vitorias": int(celulas[4].strip()),
                "empates": int(celulas[5].split("[")[0].strip()), # Limpa E[i]
            ### 9 - calcular métricas de desempenho
A partir dos dados limpos, podemos calcular novas métricas de desempenho para enriquecer nossa análise:
- **Pontos**: Vitória vale 3 pontos, empate vale 1 ponto e derrota vale 0.
- **Saldo de gols**: Gols pró (marcados) menos gols contra (sofridos).
- **Aproveitamento**: Pontos conquistados divididos pelo total de pontos possíveis (jogos * 3), multiplicado por 100 e arredondado para duas casas decimais.

**Diff em relação ao passo anterior:**
```diff
         # Ignora cabeçalhos, totais e edições futuras "A definir"
         if ano != "Ano" and "Total" not in ano and jogos.isdigit():
-            dados_limpos.append({
-                "ano": int(ano),
-                "fase": celulas[1].strip(),
-                "posicao": celulas[2].strip(),
-                "jogos": int(jogos),
-                "vitorias": int(celulas[4].strip()),
-                "empates": int(celulas[5].split("[")[0].strip()), # Limpa E[i]
-                "derrotas": int(celulas[6].strip()),
-                "gols_pro": int(celulas[7].strip()),
-                "gols_contra": int(celulas[8].strip())
-            })
+            vitorias = int(celulas[4].strip())
+            empates = int(celulas[5].split("[")[0].strip())
+            derrotas = int(celulas[6].strip())
+            gols_pro = int(celulas[7].strip())
+            gols_contra = int(celulas[8].strip())
+            
+            pontos = (vitorias * 3) + empates
+            saldo_gols = gols_pro - gols_contra
+            aproveitamento = round((pontos / (int(jogos) * 3)) * 100, 2) if int(jogos) > 0 else 0.0
+
+            dados_limpos.append({
+                "ano": int(ano),
+                "fase": celulas[1].strip(),
+                "posicao": celulas[2].strip(),
+                "jogos": int(jogos),
+                "vitorias": vitorias,
+                "empates": empates,
+                "derrotas": derrotas,
+                "gols_pro": gols_pro,
+                "gols_contra": gols_contra,
+                "pontos": pontos,
+                "saldo_gols": saldo_gols,
+                "aproveitamento": aproveitamento
+            })
 
 print(dados_limpos)
```

**Código resultante:**
```python
import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"
headers = {
    "User-Agent": "GruPy Pará II Dojo De Códigos - Python 3.11.11"
}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", class_="wikitable")
rows = table.find_all("tr")

dados_limpos = []

for row in rows:
    celulas = [celula.get_text(strip=True) for celula in row.find_all(["td", "th"])]
    if len(celulas) >= 9:
        ano = celulas[0].split("[")[0].strip()
        jogos = celulas[3].strip()
        
        if ano != "Ano" and "Total" not in ano and jogos.isdigit():
            vitorias = int(celulas[4].strip())
            empates = int(celulas[5].split("[")[0].strip())
            derrotas = int(celulas[6].strip())
            gols_pro = int(celulas[7].strip())
            gols_contra = int(celulas[8].strip())
            
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

print(dados_limpos)
```

---

### 10 - salvar os dados em formato CSV
Finalmente, importamos o módulo `csv` para salvar nossa lista de dicionários contendo os dados tratados e as métricas calculadas em um arquivo local estruturado em colunas.

**Diff em relação ao passo anterior:**
```diff
+import csv
 import requests
 from bs4 import BeautifulSoup
 
@@ -46,4 +47,15 @@ for row in rows:
                 "saldo_gols": saldo_gols,
                 "aproveitamento": aproveitamento
             })
 
-print(dados_limpos)
+print(f"Total de registros coletados: {len(dados_limpos)}")
+if dados_limpos:
+    print("\nRegistros coletados por ano:")
+    for registro in dados_limpos:
+        print(f"Copa de {registro['ano']}: {registro}")
+
+    with open("brasil_copas.csv", mode="w", encoding="utf-8", newline="") as f:
+        campos = ["ano", "fase", "posicao", "jogos", "vitorias", "empates", "derrotas", "gols_pro", "gols_contra", "pontos", "saldo_gols", "aproveitamento"]
+        writer = csv.DictWriter(f, fieldnames=campos)
+        writer.writeheader()
+        writer.writerows(dados_limpos)
+    print("\nDados salvos com sucesso em 'brasil_copas.csv'!")
```

**Código resultante (Script Completo):**
```python
import csv
import requests
from bs4 import BeautifulSoup

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
    table = soup.find("table", class_="wikitable")
    
    if table:
        rows = table.find_all("tr")
        for row in rows:
            celulas = [celula.get_text(strip=True) for celula in row.find_all(["td", "th"])]
            
            if len(celulas) >= 9:
                ano = celulas[0].split("[")[0].strip()
                jogos = celulas[3].strip()
                
                if ano != "Ano" and "Total" not in ano and jogos.isdigit():
                    vitorias = int(celulas[4].strip())
                    empates = int(celulas[5].split("[")[0].strip())
                    derrotas = int(celulas[6].strip())
                    gols_pro = int(celulas[7].strip())
                    gols_contra = int(celulas[8].strip())
                    
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

    with open("brasil_copas.csv", mode="w", encoding="utf-8", newline="") as f:
        campos = [
            "ano", "fase", "posicao", "jogos", "vitorias", "empates", "derrotas", 
            "gols_pro", "gols_contra", "pontos", "saldo_gols", "aproveitamento"
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados_limpos)
    
    print("\nDados salvos com sucesso em 'brasil_copas.csv'!")
```

---

### 11 - calcular a eficiência média e desvio padrão com Pandas e NumPy
Nesta etapa extra, importamos as bibliotecas `pandas` e `numpy` para analisar os dados persistidos no CSV. Calculamos a média de gols marcados/sofridos por jogo (eficiência ofensiva/defensiva) e o desvio padrão do aproveitamento e saldo de gols (consistência de desempenho).

**Diff em relação ao passo anterior:**
```diff
@@ -77,3 +77,21 @@
     print("\nDados salvos com sucesso em 'brasil_copas.csv'!")
+
+    # --- ANÁLISE COM PANDAS E NUMPY ---
+    print("\n" + "="*40)
+    print("      ANÁLISE COM PANDAS E NUMPY")
+    print("="*40)
+    import pandas as pd
+    import numpy as np
+
+    df = pd.read_csv("brasil_copas.csv")
+
+    # 1. Eficiência Ofensiva e Defensiva Média
+    total_jogos = df["jogos"].sum()
+    efic_ofensiva = df["gols_pro"].sum() / total_jogos
+    efic_defensiva = df["gols_contra"].sum() / total_jogos
+
+    print(f"⚽ Eficiência Ofensiva Média: {efic_ofensiva:.2f} gols marcados por jogo")
+    print(f"🛡️ Eficiência Defensiva Média: {efic_defensiva:.2f} gols sofridos por jogo")
+
+    # 2. Consistência de Desempenho (Desvio Padrão)
+    std_aproveitamento = np.std(df["aproveitamento"])
+    std_saldo = np.std(df["saldo_gols"])
+
+    print(f"📊 Desvio Padrão do Aproveitamento: {std_aproveitamento:.2f}%")
+    print(f"📊 Desvio Padrão do Saldo de Gols: {std_saldo:.2f}")
```

---

### 12 - modelo matemático para chances de levar o Hexa
Para finalizar, criamos uma fórmula probabilística simples: ponderamos o aproveitamento histórico (peso 30%), o aproveitamento recente das últimas 5 Copas (peso 40%) e a dominância ofensiva/defensiva (razão de gols pró/contra normalizada com peso de 30%).

**Diff em relação ao passo anterior:**
```diff
@@ -98,3 +98,19 @@
     print(f"📊 Desvio Padrão do Saldo de Gols: {std_saldo:.2f}")
+
+    # 3. Modelo Matemático para Chances do Hexa
+    aproveitamento_historico = df["aproveitamento"].mean() / 100
+    aproveitamento_recente = df.tail(5)["aproveitamento"].mean() / 100
+    proporcao_gols = df["gols_pro"].sum() / df["gols_contra"].sum()
+    
+    eficiencia_gols = min(proporcao_gols / 3, 1.0)
+
+    probabilidade_hexa = (0.3 * aproveitamento_historico) + (0.4 * aproveitamento_recente) + (0.3 * eficiencia_gols)
+    probabilidade_hexa_percentual = min(probabilidade_hexa * 100, 100.0)
+
+    print("\n" + "="*40)
+    print("  MODELO MATEMÁTICO: CHANCES DO HEXA 🌟")
+    print("="*40)
+    print(f"📈 Aproveitamento Histórico Médio: {aproveitamento_historico * 100:.2f}%")
+    print(f"📈 Aproveitamento Recente Médio (Últimas 5 Copas): {aproveitamento_recente * 100:.2f}%")
+    print(f"⚔️  Razão de Gols Histórica (Pró/Contra): {proporcao_gols:.2f}")
+    print(f"🏆 Chances Calculadas do Brasil ganhar o Hexa: {probabilidade_hexa_percentual:.2f}%")
+    print("="*40)
```

**Código resultante (Script Completo):**
```python
import csv
import requests
from bs4 import BeautifulSoup

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
    table = soup.find("table", class_="wikitable")
    
    if table:
        rows = table.find_all("tr")
        for row in rows:
            celulas = [celula.get_text(strip=True) for celula in row.find_all(["td", "th"])]
            
            if len(celulas) >= 9:
                ano = celulas[0].split("[")[0].strip()
                jogos = celulas[3].strip()
                
                if ano != "Ano" and "Total" not in ano and jogos.isdigit():
                    vitorias = int(celulas[4].strip())
                    empates = int(celulas[5].split("[")[0].strip())
                    derrotas = int(celulas[6].strip())
                    gols_pro = int(celulas[7].strip())
                    gols_contra = int(celulas[8].strip())
                    
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
```

---

O objetivo principal é entender que web scraping não é apenas extrair dados, mas seguir um processo completo: pesquisar, avaliar, coletar, limpar, organizar e salvar/analisar informações de forma útil.
