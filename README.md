# Otimizador Simples de Rotas de Entrega

Aplicação em Python que recebe um ponto de partida e uma lista de
paradas de entrega, e calcula a **ordem de visita que minimiza a
distância total percorrida**, usando um algoritmo de otimização
combinatória (heurística vizinho mais próximo + melhoria 2-opt).

> Projeto pessoal desenvolvido para estudo e portfólio, como estudante
> de Engenharia da Computação. Os endereços e coordenadas usados são
> **fictícios**, criados para demonstrar o funcionamento do algoritmo.

## Problema

Um entregador com várias entregas para fazer numa mesma viagem
normalmente segue a ordem em que os pedidos chegaram — não a ordem
mais eficiente. Isso significa mais quilômetros rodados, mais tempo
gasto e mais combustível/bateria consumidos do que o necessário.

## Solução

O programa lê a lista de paradas, monta uma rota inicial "gulosa"
(sempre vai para o ponto não visitado mais próximo) e depois aplica
uma técnica chamada **2-opt** para melhorar essa rota, testando trocar
a ordem de trechos e mantendo a troca sempre que ela reduzir a
distância total. O resultado final é impresso no terminal, salvo em
um banco de dados local (histórico) e exportado como um relatório
visual em HTML.

Esse é um exemplo simplificado do **problema do caixeiro viajante
(TSP)** — um problema clássico de otimização onde encontrar a rota
*perfeita* é caro computacionalmente para muitas paradas, então usamos
heurísticas que dão boas soluções em tempo razoável.

## Funcionalidades

- Cálculo de rota inicial pela heurística do vizinho mais próximo
- Melhoria da rota com a heurística 2-opt (mostra o ganho obtido, em km e %)
- Estimativa de tempo total da rota, com velocidade média configurável
- Histórico de rotas calculadas, salvo em banco de dados SQLite
- Relatório visual em HTML com resumo e tabela da rota, trecho a trecho
- Validação de entrada (exige exatamente 1 ponto de partida e ao menos 1 entrega)
- **Zero dependências externas** — usa só a biblioteca padrão do Python

## Tecnologias

- **Python 3.10+** (biblioteca padrão: `csv`, `sqlite3`, `dataclasses`, `argparse`, `math`)
- **SQLite** — banco de dados embutido para o histórico de rotas, sem precisar instalar um servidor
- **HTML + CSS** — geração do relatório visual

## Estrutura do projeto

```
otimizador-rotas-entrega/
├── data/
│   └── paradas_exemplo.csv      # dataset fictício de exemplo
├── src/
│   ├── __init__.py
│   ├── modelos.py               # estrutura de dados (Parada)
│   ├── distancia.py             # cálculo de distância (Haversine)
│   ├── otimizador.py            # algoritmo: vizinho mais próximo + 2-opt
│   ├── db.py                    # persistência do histórico (SQLite)
│   └── relatorio_html.py        # geração do relatório em HTML
├── output/                      # gerado automaticamente ao rodar main.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Como instalar

```bash
git clone https://github.com/SEU_USUARIO/otimizador-rotas-entrega.git
cd otimizador-rotas-entrega
```

Não há dependências para instalar — o projeto roda com Python puro.
(Se quiser, pode criar um ambiente virtual mesmo assim, por organização:)

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

## Como executar

Com o dataset de exemplo (já incluso):

```bash
python main.py
```

Com seu próprio arquivo de paradas (mesmo formato: `nome, latitude, longitude, tipo`):

```bash
python main.py --csv data/minhas_paradas.csv --velocidade 30
```

## Exemplo de uso

Entrada (`data/paradas_exemplo.csv`, resumida):

```csv
nome,latitude,longitude,tipo
Restaurante Sabor Caseiro,-23.5000,-51.1000,partida
Cliente - Rua das Flores 120,-23.4850,-51.0950,entrega
Cliente - Av. Central 45,-23.5300,-51.1400,entrega
...
```

Saída no terminal:

```
Ponto de partida: Restaurante Sabor Caseiro
Paradas de entrega: 10

Rota otimizada:
  0. Restaurante Sabor Caseiro
  1. Cliente - Av. das Palmeiras 210
  2. Cliente - Rua das Flores 120
  ...

Distância antes do 2-opt (ordem gulosa): 19.65 km
Distância depois do 2-opt (rota final):   18.34 km
Redução obtida pelo 2-opt: 1.31 km (6.7%)
Tempo estimado da rota final: 44 min (a 25.0 km/h)

Relatório visual salvo em output/relatorio_rota.html

Últimas rotas calculadas (histórico salvo em SQLite):
  [2026-08-26T02:47:06] 10 paradas | 19.65 km -> 18.34 km (economia: 1.31 km)
```

O arquivo `output/relatorio_rota.html` traz um resumo visual (cartões
com total de paradas, distância, tempo estimado e % de redução) e uma
tabela trecho a trecho da rota.

*(Adicione aqui um screenshot do relatório HTML depois de rodar o projeto: `output/relatorio_rota.html`.)*

## O que eu aprendi

- Como funciona uma heurística de otimização combinatória (vizinho
  mais próximo) e por que, para problemas como o do caixeiro viajante,
  encontrar a solução *ótima exata* fica caro demais para muitas paradas.
- Como implementar e entender a lógica do 2-opt: testar inversões de
  trecho e manter só as que melhoram o resultado.
- Uso do SQLite como banco de dados embutido, sem precisar configurar
  um servidor — bom para projetos pequenos ou protótipos.
- Como gerar um relatório HTML simples diretamente do Python, sem
  frameworks, usando apenas strings formatadas e CSS básico.
- A importância de validar a entrada (ex: exigir exatamente 1 ponto de
  partida) antes de rodar qualquer lógica de negócio.

## Limitações

- A distância é calculada em linha reta (Haversine), não a distância
  real por ruas — em uma cidade real, a rota "mais curta em linha reta"
  pode não ser a mais rápida de dirigir.
- O 2-opt melhora a rota, mas não garante encontrar a solução ótima
  global — para poucas paradas (como no exemplo, 10), o ganho tende a
  ser pequeno; o benefício cresce mais em cenários com mais paradas e
  rotas mais desorganizadas.
- Não há geocodificação: os endereços precisam já vir com latitude e
  longitude — não é possível digitar só "Rua X, 123" e obter a rota.
- O histórico fica em um arquivo SQLite local; não há interface para
  visualizá-lo além do terminal.

## Possíveis melhorias futuras

- Adicionar geocodificação (endereço → coordenadas) usando uma API
  gratuita como o Nominatim (OpenStreetMap).
- Exibir a rota otimizada em um mapa interativo (ex: com Leaflet.js) em vez de só uma tabela.
- Permitir múltiplos entregadores e dividir as paradas entre eles.
- Considerar janelas de horário de entrega (algumas entregas mais urgentes que outras).
- Adicionar testes automatizados (pytest) para o algoritmo de otimização.
- Trocar o SQLite por PostgreSQL caso o projeto precise rodar em múltiplas máquinas ao mesmo tempo.

---

## Perguntas que podem aparecer em uma entrevista

**1. Por que você não calculou todas as rotas possíveis para achar a melhor de verdade?**
*O que avaliam:* entendimento de complexidade computacional.
*Resposta simples:* porque o número de rotas possíveis cresce fatorialmente com o número de paradas — com 10 paradas já são milhões de combinações, e ficaria inviável calcular todas à medida que o número cresce.
*Explicação:* esse é o problema do caixeiro viajante (TSP), conhecido por ser "NP-difícil". Para poucas paradas dá pra força bruta, mas isso não escala. Por isso usei uma heurística: uma solução rápida e boa, mesmo que não seja garantidamente a melhor possível.

**2. O que é a heurística do "vizinho mais próximo" e qual sua limitação?**
*O que avaliam:* entendimento do algoritmo usado, não decoreba.
*Resposta simples:* a cada passo, o algoritmo escolhe ir para a parada não visitada mais próxima do ponto atual. A limitação é que decisões "gulosas" no começo podem obrigar a rota a fazer um trajeto ruim no final.
*Explicação:* é como escolher sempre o caminho mais curto imediato, sem pensar no restante do trajeto — às vezes isso "prende" a rota numa posição ruim mais tarde. É por isso que aplico o 2-opt depois, para corrigir esses erros.

**3. Como funciona o 2-opt que você implementou?**
*O que avaliam:* se você realmente entende a lógica do próprio código.
*Resposta simples:* o algoritmo testa inverter trechos da rota (por exemplo, trocar a ordem de visita entre a parada 3 e a 7) e mantém a inversão só se ela reduzir a distância total. Repete até não conseguir mais melhorar.
*Explicação:* isso "desfaz cruzamentos" na rota — se a rota gulosa faz um caminho que se cruza (visualmente pareceria um "X" no mapa), o 2-opt tende a encontrar e desfazer esse cruzamento, porque uma rota sem cruzamentos geralmente é mais curta.

**4. Por que você escolheu SQLite em vez de PostgreSQL para o histórico?**
*O que avaliam:* capacidade de escolher a ferramenta certa pro tamanho do problema, sem inflar tecnologia à toa.
*Resposta simples:* porque o projeto roda localmente, sozinho, sem múltiplos usuários simultâneos — o SQLite atende perfeitamente sem exigir instalar e configurar um servidor de banco separado.
*Explicação:* adicionar PostgreSQL aqui só pra "parecer mais profissional" seria complexidade desnecessária. Documentei isso no README como uma melhoria futura, caso o projeto precisasse rodar em mais de uma máquina ao mesmo tempo — aí sim faria sentido migrar.

**5. O que aconteceria se o CSV de entrada tivesse duas linhas com tipo="partida"?**
*O que avaliam:* tratamento de erros e validação de entrada.
*Resposta simples:* o programa não deixa passar — ele verifica explicitamente se existe exatamente 1 ponto de partida e mostra uma mensagem de erro clara, em vez de tentar adivinhar qual usar.
*Explicação:* isso evita comportamento ambíguo. Prefiro que o programa avise o problema claramente do que silenciosamente escolher a primeira "partida" e gerar um resultado que o usuário não esperava.

**6. Por que a distância calculada não é 100% igual à distância real dirigindo?**
*O que avaliam:* consciência das limitações do próprio projeto.
*Resposta simples:* porque uso a fórmula de Haversine, que calcula a distância em linha reta entre dois pontos — não considera ruas, mão única, ou obstáculos.
*Explicação:* calcular a distância real de rota exigiria uma API de mapas (como Google Maps ou OSRM), que tem custo ou limites de uso. Para o propósito do projeto — mostrar o algoritmo de otimização — a distância em linha reta já é suficiente e deixei essa limitação clara no README.

**7. Como você testou que o código realmente funciona?**
*O que avaliam:* prática de testes, mesmo que informal.
*Resposta simples:* rodei o programa com o dataset de exemplo, verifiquei que a distância depois do 2-opt é sempre menor ou igual à distância antes, rodei duas vezes pra confirmar que o histórico acumula corretamente, e testei também um CSV inválido pra ver se o erro é tratado direito.
*Explicação:* não tenho testes automatizados (pytest) ainda — isso está na lista de melhorias futuras — mas testei manualmente os casos principais e os casos de erro antes de considerar o projeto pronto.

**8. Por que separar o código em `otimizador.py`, `db.py` e `relatorio_html.py` em vez de um único arquivo?**
*O que avaliam:* organização de código.
*Resposta simples:* cada arquivo cuida de uma responsabilidade: o algoritmo de otimização, a persistência de dados e a geração do relatório visual. Isso facilita entender e modificar cada parte isoladamente.
*Explicação:* se eu quiser trocar SQLite por outro banco, mexo só em `db.py`. Se quiser mudar o visual do relatório, mexo só em `relatorio_html.py`. O `main.py` só orquestra as peças.

**9. O que esse projeto tem a ver com o problema real de uma empresa de delivery?**
*O que avaliam:* conexão entre o projeto técnico e um problema de negócio real.
*Resposta simples:* simula, em pequena escala, um problema real de logística: decidir em que ordem visitar vários pontos de entrega para minimizar distância e tempo, o que impacta custo operacional e satisfação do cliente.
*Explicação:* empresas de logística e delivery resolvem versões muito mais complexas desse mesmo problema (com múltiplos entregadores, janelas de tempo, trânsito em tempo real) — mas o núcleo do problema, otimizar uma sequência de visitas, é o mesmo que implementei aqui de forma simplificada.

**10. Você usou alguma IA generativa para gerar coordenadas geográficas fictícias?**
*O que avaliam:* transparência sobre como o projeto foi construído.
*Resposta simples:* as coordenadas do dataset de exemplo são fictícias, criadas manualmente para simular um cenário plausível de entregas numa área pequena — não vêm de nenhum endereço real.
*Explicação:* isso é importante deixar claro numa entrevista: os dados são um cenário de demonstração, não uma coleta real de endereços, e isso está documentado no README.

---

## Sugestões para o GitHub

**Nome do repositório:** `otimizador-rotas-entrega`

**Descrição curta:**
> Otimizador de rotas de entrega em Python (heurística vizinho mais próximo + 2-opt), com histórico em SQLite e relatório visual em HTML.

**Topics sugeridos:**
`python` `algoritmos` `otimizacao` `logistica` `sqlite` `heuristica` `travelling-salesman-problem` `portfolio`
