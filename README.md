# Caixeiro Viajante (TSP) - Visualizador Interativo

Este projeto é uma aplicação interativa que resolve e visualiza o Problema do Caixeiro Viajante (TSP - *Traveling Salesperson Problem*). Ele permite adicionar cidades em um mapa com o mouse e comparar em tempo real o desempenho, o custo e as rotas de dois algoritmos diferentes: **Força Bruta** (solução exata) e **Busca Gulosa** (heurística do vizinho mais próximo).

## Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Gerenciador de Pacotes:** [uv](https://github.com/astral-sh/uv) (Extremamente rápido, desenvolvido pela Astral)
*   **Interface Gráfica:** `pygame-ce` (Pygame Community Edition - um *fork* mais moderno e otimizado do Pygame original)

## Pré-requisitos

Para rodar este projeto, você precisa ter o gerenciador `uv` instalado na sua máquina. Se ainda não o tem, você pode instalá-lo conforme a [documentação oficial](https://github.com/astral-sh/uv) (por exemplo, usando `curl -LsSf https://astral.sh/uv/install.sh | sh` no Linux/macOS ou via `pip install uv`).

## Como Executar o Projeto

Como estamos utilizando o `uv`, você não precisa configurar um ambiente virtual complexo manualmente. O `uv` pode baixar as dependências e executar o script em um único comando.

No seu terminal, navegue até a pasta onde o arquivo `main.py` está salvo e execute o seguinte comando:

```bash
uv run --with pygame-ce main.py
```

### Alternativa: Criando um ambiente virtual explícito com `uv`

Se preferir criar um ambiente virtual clássico, siga os passos:

1. Crie o ambiente virtual:
   ```bash
   uv venv
   ```
2. Ative o ambiente virtual:
   * **Windows:** `.venv\Scripts\activate`
   * **Linux/macOS:** `source .venv/bin/activate`
3. Instale o `pygame-ce`:
   ```bash
   uv pip install pygame-ce
   ```
4. Execute o jogo:
   ```bash
   python main.py
   ```

## Como Usar a Aplicação

1. **Adicionar Cidades:** Com a aplicação aberta, clique em qualquer espaço em branco na área superior (mapa) para criar uma nova cidade. O custo de viagem entre as cidades será gerado aleatoriamente nos bastidores.
2. **Força Bruta:** Clique no botão vermelho para rodar o algoritmo exato. **Atenção:** Evite passar de 10-11 cidades, pois a complexidade matemática $O(N!)$ fará o programa travar devido à quantidade colossal de caminhos testados.
3. **Busca Gulosa:** Clique no botão azul para rodar o algoritmo do Vizinho Mais Próximo. Este algoritmo suporta dezenas de cidades instantaneamente, mas a rota final pode não ser a mais otimizada.
4. **Analisar Estatísticas:** Observe o painel inferior para verificar o **Custo Total**, o **Tempo de Execução** em segundos e a **Ordem Percorrida** para cada algoritmo. Os custos individuais de cada trecho aparecerão desenhados em cima das linhas conectivas no mapa.
5. **Limpar:** Utilize o botão "Limpar Tudo" para zerar o mapa e iniciar uma nova simulação.