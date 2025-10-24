# Avaliação de Desempenho do Spring PetClinic (Microservices) com Locust

Este repositório contém os artefatos para a avaliação de desempenho da aplicação Spring PetClinic (versão microsserviços), conforme solicitado no Trabalho 07.

## Objetivo

[cite_start]O objetivo deste trabalho é medir e relatar o desempenho básico da aplicação Spring PetClinic (versão microsserviços) usando a ferramenta de teste de carga Locust[cite: 4].

## Aplicação-Alvo

* [cite_start]**Aplicação:** Spring PetClinic - Microservices [cite: 14]
* [cite_start]**Repositório Original:** `https://github.com/spring-petclinic/spring-petclinic-microservices` [cite: 15]

---

## Passos de Reprodução

[cite_start]Esta seção detalha os passos necessários para configurar o ambiente e reproduzir os testes de carga[cite: 41].

**Nota Importante:** A execução padrão (`docker compose up`) consome uma quantidade muito grande de recursos (RAM). Os passos abaixo utilizam um **modo híbrido** (serviços de infra no Docker, serviços Java locais) para permitir a execução em máquinas com 8GB de RAM.

### 1. Pré-requisitos

Antes de começar, garanta que você tem os seguintes softwares instalados:

* **Git** (e **Git Bash**, que é obrigatório para rodar os scripts)
* **Docker Desktop** (em execução)
* **Java JDK 17** (com a variável de ambiente `JAVA_HOME` configurada)
* **Python 3.8** (ou superior)
* **Locust** (`pip install locust`)
* Bibliotecas Python para análise (ex: `pandas`, `matplotlib` - para o script `plot_locust_results`)

### 2. Configuração do Ambiente (Como subir o sistema)

1.  **Clonar este repositório:**
    ```bash
    git clone [URL-DO-SEU-REPOSITORIO]
    cd [NOME-DA-PASTA-DO-REPOSITORIO]
    ```

2.  **Verificar Conflitos de Porta:**
    A aplicação roda na porta `8080`. Se você tiver outros serviços (como um `pgAdmin` de outro projeto) usando esta porta, pare-os primeiro.
    ```bash
    # Exemplo de como parar um pgAdmin que estava em conflito
    docker stop pgadmin_web
    ```

3.  **Iniciar a Aplicação (Modo Híbrido):**
    Abra o **Git Bash** na pasta do projeto e execute o script de inicialização.
    ```bash
    ./scripts/run_all.sh
    ```
    *O terminal exibirá a mensagem `Waiting for apps to start`. Este processo é demorado (5-10 minutos). Deixe este terminal aberto.*

4.  **Verificar a Aplicação:**
    Após alguns minutos, acesse `http://localhost:8080/` no seu navegador. Se a página do PetClinic carregar, o sistema está pronto.

### 3. Execução dos Cenários de Teste

Com a aplicação rodando (Passo 2), abra um **NOVO** terminal Git Bash na mesma pasta do projeto para executar os testes do Locust.

O arquivo `locustfile.py` deste repositório já está configurado com os caminhos de API corretos (ex: `/api/customer/owners`).

#### Cenário A (Leve)

* [cite_start]**Carga:** 50 usuários, 10 minutos de duração[cite: 23].
* **Comando:**
    ```bash
    # Este comando executa uma rodada. Para o trabalho, ele foi executado 10 vezes,
    # mudando o nome do arquivo de saída (ex: run1, run2, ...)
    locust -f locustfile.py --users 50 --spawn-rate 5 --run-time 10m --headless --csv=results/cenario_a/run1
    ```

#### Cenário B (Moderado)

* [cite_start]**Carga:** 100 usuários, 10 minutos de duração[cite: 24].
* **Comando:**
    ```bash
    # Executar 10 vezes, mudando o nome do arquivo de saída.
    locust -f locustfile.py --users 100 --spawn-rate 10 --run-time 10m --headless --csv=results/cenario_b/run1
    ```

#### Cenário C (Pico)

* [cite_start]**Carga:** 200 usuários, 5 minutos de duração[cite: 25].
* **Comando:**
    ```bash
    # Executar 10 vezes, mudando o nome do arquivo de saída.
    locust -f locustfile.py --users 200 --spawn-rate 20 --run-time 5m --headless --csv=results/cenario_c/run1
    ```

---

## [cite_start]Estrutura do Repositório [cite: 35]

* [cite_start]`locustfile.py`: O script Python com as tarefas de teste do Locust[cite: 38].
* `plot_locust_results.py`: Script Python desenvolvido para ler os CSVs da pasta `results/`, calcular as médias e gerar os gráficos comparativos entre os cenários.
* [cite_start]`results/`: Pasta contendo os resultados brutos dos testes[cite: 40].
    * `cenario_a/`: Contém os 10 arquivos CSV do Cenário A.
    * `cenario_b/`: Contém os 10 arquivos CSV do Cenário B.
    * `cenario_c/`: Contém os 10 arquivos CSV do Cenário C.
