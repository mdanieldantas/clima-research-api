# API de Pesquisa em Clima – Regras para IA

Este arquivo existe para ajudar ferramentas de IA (Copilot, etc.) a entender a arquitetura do projeto e seguir as convenções corretas ao gerar código.

## 1. Visão geral do projeto

- Nome: API de Pesquisa em Clima.
- Objetivo: integrar dados geográficos (cidades/UF) e dados climáticos, com histórico de consultas e apoio a séries temporais.
- Uso principal: portfólio técnico e estudo de desenvolvimento assistido por IA, com foco em clima e meio ambiente.
- Estilo: API REST que responde **apenas JSON**, sem HTML padrão do framework.

## 2. Stack técnica

- Linguagem: Python.
- Framework Web: FastAPI.
- HTTP client para APIs externas: httpx.
- ORM/Persistência: SQLAlchemy.
- Banco de dados atual: SQLite (planejado para evoluir para PostgreSQL).
- Testes: pytest.
- Documentação: README, INTEGRANTES, coleção Postman, arquivos .md de arquitetura.

## 3. Estrutura de pastas (alto nível)

A estrutura esperada é:

- `src/main.py`  
  Cria a aplicação FastAPI, configura CORS, define porta 3000 e registra os routers.

- `src/core/`  
  - `config.py` – configuração geral (ex.: porta, env vars, URLs externas).  
  - `database.py` – criação do engine/session do SQLAlchemy.  
  - `exceptions.py` – exceções de domínio/personalizadas.  
  - `handlers.py` – handlers globais de erro para FastAPI.

- `src/api/routes/`  
  Arquivos de rotas, um por área:
  - `health.py` – `GET /api/v1/health`.  
  - `clima.py` – `GET /api/v1/clima/{nome_cidade}`.  
  - `cidades.py` – `GET /api/v1/cidades/{sigla_uf}`.  
  - `historico.py` – `GET /api/v1/historico/{nome_cidade}`.  
  - `serie.py` – `GET /api/v1/serie/{nome_cidade}`.

- `src/schemas/`  
  Schemas Pydantic para requests/responses:
  - `health.py`, `clima.py`, `cidade.py`, `historico.py`, `serie.py`, `error.py`.

- `src/services/`  
  Regras de negócio e integração externa:
  - `city_service.py` – busca cidades / UF em APIs públicas (IBGE, Brasil API).  
  - `weather_service.py` – consulta clima em Open‑Meteo, usando latitude/longitude.  
  - `history_service.py` – grava e lê histórico de consultas.  
  - `series_service.py` – monta séries temporais a partir do histórico.

- `src/repositories/`  
  - `history_repository.py` – opera a tabela de histórico (query_history) via SQLAlchemy.

- `src/models/`  
  - `query_history.py` – modelo SQLAlchemy com campos:
    - id, city_name, state_code, latitude, longitude,
      weather_summary, temperature, temperature_min, temperature_max,
      queried_at, source_city_api, source_weather_api.

- `src/utils/`  
  Utilitários puros:
  - `validators.py` – validações de entrada (nome de cidade, sigla de UF).  
  - `datetime_utils.py` – helpers para datas/horários (ex.: normalizar para UTC).

- `tests/`  
  - `test_health.py`, `test_clima.py`, `test_cidades.py`, `test_historico.py`, `test_serie.py` (se existir).

- `docs/`  
  - `postman_collection.json` e outros artefatos de documentação.

## 4. Regras obrigatórias para a IA seguir

Ao gerar ou modificar código neste projeto, **sempre seguir**:

1. **Respostas sempre em JSON**  
   - Não retornar HTML padrão do FastAPI/Starlette.
   - Erros devem usar um schema de erro padronizado (`schemas/error.py`), com campos como `code`, `message`, `details`.

2. **Endereços e rotas**
   - Prefixo padrão: `/api/v1/...`.
   - Não criar rotas fora de `src/api/routes/`.
   - Toda rota deve ter um schema de resposta Pydantic associado em `src/schemas/`.

3. **Sem coordenadas fixas em código**
   - Nunca hard‑codar latitude/longitude.
   - Sempre resolver coordenadas dinamicamente a partir do nome da cidade, usando APIs públicas (IBGE/Brasil API → coordenadas → Open‑Meteo).

4. **Integrações externas**
   - Buscar cidades/UF:
     - Preferir IBGE Localidades ou Brasil API, tratando erros de rede/timeouts.
   - Buscar clima:
     - Usar Open‑Meteo (ou API equivalente), aproveitando suporte a dados históricos/séries temporais.
   - Em caso de falha em serviços externos, retornar HTTP 503 com payload de erro padronizado.

5. **Persistência e histórico**
   - Toda consulta bem‑sucedida de clima deve ser registrada em `query_history`.
   - A camada de acesso a banco deve passar por `repositories`, não diretamente dos `routes`.
   - `queried_at` deve registrar a data/hora da consulta (idealmente em UTC).

6. **Validações**
   - Nome de cidade: mínimo 2 caracteres, string não vazia.
   - Sigla de UF: exatamente 2 letras (A–Z).
   - Entradas inválidas → retornar HTTP 400 com payload padronizado.

7. **Códigos de erro HTTP**
   - `400` – entrada inválida (ex.: UF inválida, city name muito curto).  
   - `404` – cidade ou UF não encontrada nas APIs externas ou no histórico.  
   - `503` – serviço externo indisponível (falha de rede, timeout, erro na API de clima ou cidades).

8. **Testes**
   - Toda nova rota ou alteração relevante deve ter testes em `tests/`.
   - Usar pytest e TestClient da FastAPI.
   - Não remover testes existentes a menos que for estritamente necessário e justificado.

## 5. Como a IA deve estruturar o código

- Funções de rota (em `src/api/routes`) devem ser finas:
  - validar inputs,
  - chamar serviços,
  - traduzir resultados para schemas de resposta,
  - levantar exceções de domínio quando necessário.

- Serviços (em `src/services`) devem:
  - encapsular regras de negócio,
  - falar com APIs externas via httpx,
  - não conhecer FastAPI diretamente (sem `Request`, `Response` ou `Depends` aqui).

- Repositórios (em `src/repositories`) devem:
  - lidar com sessão de banco,
  - expor funções claras (`save_query_history`, `list_history_by_city`, etc.).

- Modelos (em `src/models`) devem:
  - corresponder à estrutura de banco atual,
  - não conter lógica de negócio complexa.

## 6. Documentos adicionais (para carregar sob demanda)

Quando precisar de mais detalhes, a IA deve procurar por arquivos como:

- `README.md` – visão geral do projeto e instruções de uso.  
- `docs/ROUTES_GUIDELINES.md` – padrões mais detalhados para rotas (se existir).  
- `docs/PERSISTENCE_GUIDELINES.md` – detalhes de migração para PostgreSQL, padrões de SQLAlchemy (se existir).  
- `docs/ERROR_HANDLING.md` – design dos payloads de erro e estratégias de logging (se existir).

Se estes arquivos ainda não existirem, a IA pode ser instruída a criá‑los como parte de tarefas futuras.