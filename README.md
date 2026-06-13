# Coding Dojo: Web Scraping com Python

## Desempenho do Brasil nas últimas Copas do Mundo

## Horário

**09:00 às 11:30**

## Objetivo do Dojo

Neste dojo, vamos praticar o fluxo completo de uma coleta de dados na web usando Python.

O tema será o **desempenho da Seleção Brasileira nas últimas Copas do Mundo**. A ideia é pesquisar fontes de dados, estudar a estrutura dos sites, executar extrações com `requests` e `BeautifulSoup`, organizar as informações e salvar o resultado em um arquivo CSV.

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
+for ano in [2006, 2010, 2014, 2018, 2022]:
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

for ano in [2006, 2010, 2014, 2018, 2022]:
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
 
 for ano in [2006, 2010, 2014, 2018, 2022]:
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

for ano in [2006, 2010, 2014, 2018, 2022]:
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
 
-for ano in [2006, 2010, 2014, 2018, 2022]:
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
                "derrotas": int(celulas[6].strip()),
                "gols_pro": int(celulas[7].strip()),
                "gols_contra": int(celulas[8].strip())
            })

print(dados_limpos)
```

---

# Cronograma dos Rounds

## 09:00 - 09:10

# Abertura do Dojo

## Objetivo

Apresentar o tema, explicar a dinâmica do dojo e alinhar o resultado esperado.

## Explicação

Antes de começar a escrever código, o grupo deve entender o problema: queremos coletar dados sobre o desempenho do Brasil nas últimas Copas do Mundo e transformar essas informações em uma base organizada.

## Resultado esperado

Todos devem entender o objetivo final:

```text
Encontrar uma fonte de dados
Estudar a página
Extrair informações
Limpar os dados
Salvar em CSV
```

---

## 09:10 - 09:30

# ROUND 1: Pesquisar fontes de dados

## Objetivo

Encontrar páginas que tenham dados sobre o Brasil nas Copas do Mundo.

## Explicação

Web scraping começa antes do código. Primeiro precisamos descobrir onde os dados estão disponíveis e se a fonte é adequada para coleta.

## Tarefas

```text
Pesquisar páginas sobre o Brasil nas Copas
Comparar possíveis fontes
Verificar se os dados estão visíveis na página
Identificar se existem tabelas ou listas
Escolher a fonte principal do dojo
```

## Perguntas para guiar

```text
O site está em português?
Os dados aparecem diretamente na página?
Existe tabela HTML?
Precisa de login?
O conteúdo carrega com JavaScript?
A página parece boa para usar com requests e BeautifulSoup?
```

## Resultado esperado

Escolher uma fonte principal de dados para a extração.

---

## 09:30 - 09:50

# ROUND 2: Estudar a estrutura do site

## Objetivo

Entender como os dados estão organizados dentro da página.

## Explicação

Depois de escolher a fonte, o grupo deve estudar a estrutura HTML da página. O objetivo é encontrar onde estão as tabelas, linhas, colunas e informações úteis.

## Tarefas

```text
Abrir a página no navegador
Usar a opção Inspecionar
Localizar as tabelas da página
Identificar quais dados serão coletados
Anotar os nomes das colunas importantes
```

## Dados desejados

```text
Ano
Fase
Posição
Jogos
Vitórias
Empates
Derrotas
Gols marcados
Gols sofridos
```

## Resultado esperado

Saber qual tabela ou seção da página contém os dados que serão raspados.

---

## 09:50 - 10:10

# ROUND 3: Fazer a primeira requisição com requests

## Objetivo

Acessar a página usando Python.

## Explicação

Neste round, o grupo começa a parte prática. Vamos usar a biblioteca `requests` para baixar o HTML da página escolhida.

## Exemplo

```python
import requests

url = "https://pt.wikipedia.org/wiki/Brasil_na_Copa_do_Mundo_FIFA"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    resposta = requests.get(url, headers=headers)
    resposta.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer requisição: {e}")
    exit(1)

print(resposta.status_code)
print(resposta.text[:500])
```

## Tarefas

```text
Fazer a requisição HTTP
Verificar o status da resposta
Exibir uma parte do HTML
Confirmar se a página foi carregada corretamente
```

## Resultado esperado

A página deve ser acessada com sucesso pelo Python.

---

## 10:10 - 10:30

# ROUND 4: Encontrar as tabelas com BeautifulSoup

## Objetivo

Usar BeautifulSoup para localizar as tabelas da página.

## Explicação

Com o HTML carregado, vamos usar `BeautifulSoup` para navegar pela estrutura da página e encontrar os elementos que contêm os dados.

## Exemplo

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(resposta.text, "html.parser")

tabelas = soup.find_all("table")

print(f"Total de tabelas encontradas: {len(tabelas)}")
```

## Tarefas

```text
Criar o objeto BeautifulSoup
Buscar todas as tabelas da página
Exibir a quantidade de tabelas encontradas
Inspecionar o conteúdo das primeiras tabelas
Identificar a tabela correta
```

## Resultado esperado

Encontrar a tabela que contém os dados do desempenho do Brasil nas Copas.

---

## 10:30 - 10:50

# ROUND 5: Executar a extração dos dados

## Objetivo

Extrair os dados da tabela escolhida.

## Explicação

Neste round, vamos percorrer as linhas da tabela e transformar os dados em uma lista de dicionários.

## Exemplo de estrutura

```python
dados = []

for linha in linhas:
    registro = {
        "ano": "",
        "fase": "",
        "jogos": "",
        "vitorias": "",
        "empates": "",
        "derrotas": "",
        "gols_marcados": "",
        "gols_sofridos": ""
    }

    dados.append(registro)
```

## Tarefas

```text
Percorrer as linhas da tabela
Extrair as células de cada linha
Remover espaços extras
Criar um dicionário para cada Copa
Guardar os registros em uma lista
```

## Resultado esperado

Uma lista com os dados brutos das participações do Brasil nas Copas.

---

## 10:50 - 11:05

# ROUND 6: Limpar e organizar os dados

## Objetivo

Preparar os dados para análise.

## Explicação

Dados extraídos da web geralmente precisam de limpeza. Podemos encontrar quebras de linha, textos extras, símbolos e números em formato de texto.

## Tarefas

```text
Padronizar nomes das colunas
Remover quebras de linha
Remover espaços extras
Converter números
Tratar campos vazios
Filtrar apenas as últimas Copas
```

## Copas sugeridas para análise

```text
2006
2010
2014
2018
2022
```

## Resultado esperado

Uma base organizada contendo apenas os dados das últimas Copas do Mundo.

---

## 11:05 - 11:20

# ROUND 7: Calcular métricas e salvar em CSV

## Objetivo

Criar métricas simples de desempenho e salvar os dados em CSV.

## Explicação

Depois da limpeza, podemos calcular novas informações para analisar melhor o desempenho do Brasil.

## Métricas sugeridas

```text
Pontos
Saldo de gols
Média de gols marcados
Média de gols sofridos
Aproveitamento
```

## Regras

```text
Vitória = 3 pontos
Empate = 1 ponto
Derrota = 0 pontos
```

## Fórmulas

```text
pontos = (vitórias * 3) + empates

saldo_de_gols = gols_marcados - gols_sofridos

aproveitamento = pontos / (jogos * 3) * 100
```

## Exemplo para salvar em CSV

```python
import pandas as pd

df = pd.DataFrame(dados)

df.to_csv("brasil_ultimas_copas.csv", index=False, encoding="utf-8")
```

## Resultado esperado

Gerar um arquivo:

```text
brasil_ultimas_copas.csv
```

contendo os dados tratados e as métricas calculadas.

---

## 11:20 - 11:30

# Encerramento e retrospectiva

## Objetivo

Revisar o que foi feito e discutir melhorias.

## Explicação

O encerramento serve para consolidar o aprendizado. O grupo deve refletir sobre o processo completo: desde a pesquisa da fonte até a geração do CSV.

## Perguntas para discussão

```text
A fonte escolhida foi boa?
O que facilitou a extração?
O que dificultou a extração?
O que poderia quebrar esse scraper no futuro?
Como deixar o código mais organizado?
Como salvar também em JSON?
Como transformar esses dados em gráficos?
Como criar uma API com esses dados?
```

## Resultado esperado

O grupo finaliza o dojo com um arquivo CSV gerado e uma visão clara do processo de web scraping.

---

# Resultado final esperado

Ao final do dojo, o grupo terá praticado:

```text
Pesquisa de fontes de dados
Estudo da estrutura de sites
Uso de requests
Uso de BeautifulSoup
Extração de tabelas HTML
Limpeza de dados
Cálculo de métricas
Exportação para CSV
```

O objetivo principal é entender que web scraping não é apenas extrair dados, mas seguir um processo completo: pesquisar, avaliar, coletar, limpar, organizar e salvar informações de forma útil.
