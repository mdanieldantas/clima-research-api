# Tasks: api-pesquisa-clima

> Nota: antes de começar qualquer tarefa, crie uma branch de feature a partir de `dev` seguindo a convenção do projeto (ex.: `feature/T04-query-history`). Exemplo rápido:

```bash
git checkout dev
git pull --ff-only origin dev
git checkout -b feature/T04-query-history
```


Este arquivo lista tarefas atômicas (cada uma adequada para um commit/PR único) para implementar a feature `api-pesquisa-clima`. Todas as tarefas estão em português (pt-BR).

Formato de cada tarefa:
- ID: identificador único.
- Título: breve.
- What: o que será feito.
- Where: arquivos/módulos criados ou modificados.
- Depends on: dependências de outras tasks.
- Reuses: componentes existentes a serem reaproveitados.
- Done when: critérios objetivos de pronto.
- Tests: quais testes rodar e comandos.

---

### T01 — Setup base da API e health
- ID: T01
- Título: Criar aplicação FastAPI básica, CORS e endpoint de health
- What: Inicializar `FastAPI`, configurar CORS básico, registrar router `health` com endpoint `GET /api/v1/health` que retorna JSON de status, versão e timestamp.
- Where:
  - `src/main.py`
  - `src/api/routes/health.py`
  - `src/core/config.py` (variáveis de ambiente básicas)
- Depends on: —
- Reuses: —
- Done when:
  - `uvicorn src.main:app` sobe sem erro.
  - `GET /api/v1/health` responde 200 com JSON `{status, versao, timestamp, banco_dados}`.
- Tests:
  - `tests/test_health.py` (TestClient)
  - Executar: `pytest tests/test_health.py -q`

---

### T02 — Configuração core e fábrica de banco de dados
- ID: T02
- Título: Implementar `config` e `database` (engine/session)
- What: Criar arquivo de configuração que lê URL do DB via env var e implementar `engine` + `SessionLocal`/`sessionmaker` em `src/core/database.py` com padrão SQLite para dev.
- Where:
  - `src/core/config.py`
  - `src/core/database.py`
- Depends on: T01
- Reuses: —
- Done when:
  - Há função/fábrica para obter sessão e criar engine usando URL configurável.
  - Teste de conexão simples consegue abrir/fechar sessão.
- Tests:
  - `tests/test_database.py` que importa `get_engine`/`SessionLocal` e cria tabela temporária
  - Executar: `pytest tests/test_database.py -q`

---

### T03 — Schemas Pydantic (contratos de API)
- ID: T03
- Título: Definir schemas Pydantic para responses e erros
- What: Criar os schemas: `ClimaResponse`, `CidadeResponse`, `HistoricoItem`, `SerieResponse`, `ErrorResponse` conforme `spec.md` e `error-handling.md`.
- Where:
  - `src/schemas/clima.py`
  - `src/schemas/cidade.py`
  - `src/schemas/historico.py`
  - `src/schemas/serie.py`
  - `src/schemas/error.py`
- Depends on: T01
- Reuses: `.specs/features/api-pesquisa-clima/spec.md` (contratos)
- Done when:
  - Os módulos podem ser importados sem erro.
  - `ErrorResponse` tem campos `status`, `error_code`, `message`, `details`.
- Tests:
  - `tests/test_schemas.py` validações básicas de instância/serialização
  - Executar: `pytest tests/test_schemas.py -q`

---

### T04 — Modelo SQLAlchemy `query_history`
- ID: T04
- Título: Criar modelo SQLAlchemy para `query_history`
- What: Implementar `src/models/query_history.py` com os campos obrigatórios (id, city_name, state_code, latitude, longitude, weather_summary, temperature, temperature_min, temperature_max, queried_at, source_city_api, source_weather_api).
- Where:
  - `src/models/query_history.py`
- Depends on: T02, T03
- Reuses: `src/core/database.py` (Base/engine)
- Done when:
  - Modelo definido e `Base.metadata.create_all(engine)` cria tabela no DB de dev.
- Tests:
  - `tests/test_models.py` usando engine in-memory cria tabela e instancia `query_history`.
  - Executar: `pytest tests/test_models.py -q`

---

### T05 — Repositório de histórico
- ID: T05
- Título: Implementar `history_repository` (save/list/agg)
- What: Criar `src/repositories/history_repository.py` com funções: `save_query(session, payload)`, `list_by_city(session, city_name, order='desc')`, `agg_series_by_city(session, city_name)`.
- Where:
  - `src/repositories/history_repository.py`
- Depends on: T04, T02
- Reuses: `src/models/query_history.py`
- Done when:
  - Operações básicas fazem insert e consultas corretamente no SQLite in-memory.
- Tests:
  - `tests/test_history_repository.py` cobrindo salvar, listar (ordenacao) e agregacao simples.
  - Executar: `pytest tests/test_history_repository.py -q`

---

### T06 — Clientes HTTP para APIs externas (IBGE, Brasil API, Open‑Meteo)
- ID: T06
- Título: Implementar wrappers HTTP async com timeouts/retries
- What: Criar clientes em `src/clients/`:
  - `ibge_client.py` (buscar cidade/municipios por UF)
  - `brasil_api_client.py` (fallback)
  - `open_meteo_client.py` (consulta clima por lat/lon)
  - Implementar timeouts, limites de retry e logging básico.
- Where:
  - `src/clients/ibge_client.py`
  - `src/clients/brasil_api_client.py`
  - `src/clients/open_meteo_client.py`
- Depends on: T02
- Reuses: `httpx.AsyncClient` (via `src/utils/http_client.py` opcional)
- Done when:
  - Funções retornam dados normalizados ou levantam exceção específica em timeout/erro.
- Tests:
  - `tests/test_clients.py` usando `respx`/`pytest-httpx` para mockar respostas.
  - Executar: `pytest tests/test_clients.py -q`

---

### T07 — Serviço de cidades (`city_service`)
- ID: T07
- Título: Implementar resolução de cidade com fallback e normalização
- What: Implementar `src/services/city_service.py` com `resolve(nome_cidade)` e `list_by_state(sigla_uf)`. Deve normalizar nomes e usar `ibge_client` → `brasil_api_client` fallback.
- Where:
  - `src/services/city_service.py`
- Depends on: T06, T03
- Reuses: `src/clients/ibge_client.py`, `src/clients/brasil_api_client.py`, `src/utils/validators.py`
- Done when:
  - `resolve` retorna dados `{city_name, state_code, latitude, longitude, source_city_api}` para uma cidade conhecida.
  - Em cidade desconhecida, lança `NotFoundError`.
- Tests:
  - `tests/test_city_service.py` com mocks dos clients (respx)
  - Executar: `pytest tests/test_city_service.py -q`

---

### T08 — Serviço de clima (`weather_service`)
- ID: T08
- Título: Implementar consulta Open‑Meteo e normalização de resposta
- What: Implementar `src/services/weather_service.py` com `fetch_by_coords(lat, lon)` que chama `open_meteo_client` e mapeia para campos do `ClimaResponse`.
- Where:
  - `src/services/weather_service.py`
- Depends on: T06, T03
- Reuses: `src/clients/open_meteo_client.py`
- Done when:
  - `fetch_by_coords` retorna `{temperature, temperature_min, temperature_max, weather_summary, source_weather_api}` ou lança `ExternalServiceError` em falha.
- Tests:
  - `tests/test_weather_service.py` com mocks do `open_meteo_client`.
  - Executar: `pytest tests/test_weather_service.py -q`

---

### T09 — Serviço de histórico (`history_service`)
- ID: T09
- Título: Implementar gravação automática de consultas e leitura de histórico
- What: Implementar `src/services/history_service.py` que encapsula chamadas ao `history_repository` e garante `queried_at` em UTC.
- Where:
  - `src/services/history_service.py`
- Depends on: T05, T03
- Reuses: `src/repositories/history_repository.py`
- Done when:
  - `save` persiste registros com campos esperados e `list_by_city` retorna dados ordenados.
- Tests:
  - `tests/test_history_service.py` (in-memory DB)
  - Executar: `pytest tests/test_history_service.py -q`

---

### T10 — Serviço de séries (`series_service`)
- ID: T10
- Título: Implementar agregações para série temporal
- What: Implementar `src/services/series_service.py` com `aggregate(city_name, records)` produzindo `SerieResponse` com média/mínimo/máximo e intervalo de datas.
- Where:
  - `src/services/series_service.py`
- Depends on: T05, T03
- Reuses: `src/repositories/history_repository.py`
- Done when:
  - Agregações retornam valores coerentes para dataset de teste.
- Tests:
  - `tests/test_series_service.py` com dados simulados/in-memory
  - Executar: `pytest tests/test_series_service.py -q`

---

### T11 — Rotas da feature (`clima`, `cidades`, `historico`, `serie`)
- ID: T11
- Título: Criar routers e integrar serviços via Depends
- What: Implementar `src/api/routes/clima.py`, `cidades.py`, `historico.py`, `serie.py`. Declarar `response_model` usando schemas. Injetar services via `Depends`.
- Where:
  - `src/api/routes/clima.py`
  - `src/api/routes/cidades.py`
  - `src/api/routes/historico.py`
  - `src/api/routes/serie.py`
- Depends on: T03, T07, T08, T09, T10, T01
- Reuses: `src/services/*`, `src/schemas/*`
- Done when:
  - Endpoints respondem com os `response_model` esperados e levantam exceções padronizadas em entrada inválida.
- Tests:
  - `tests/test_clima.py`, `tests/test_cidades.py`, `tests/test_historico.py`, `tests/test_serie.py` (TestClient com overrides)
  - Executar: `pytest tests/test_clima.py::test_get_clima_success -q` (exemplo)

---

### T12 — Tratamento de erros global e exceções de domínio
- ID: T12
- Título: Implementar exceções de domínio e handlers globais
- What: Criar `src/core/exceptions.py` (InvalidInputError, NotFoundError, ExternalServiceError, DatabaseError) e `src/core/handlers.py` que mapeia para `ErrorResponse` e garante `status` coincidente com o HTTP status da resposta.
- Where:
  - `src/core/exceptions.py`
  - `src/core/handlers.py`
- Depends on: T03
- Reuses: `src/schemas/error.py`
- Done when:
  - Lançar `NotFoundError` em rota resulta em resposta JSON com `status`, `error_code`, `message`, `details`.
- Tests:
  - `tests/test_error_handlers.py` (TestClient e simulação de exceções)
  - Executar: `pytest tests/test_error_handlers.py -q`

---

### T13 — Utilitários: validators, normalizers e HTTP client wrapper
- ID: T13
- Título: Implementar validações e helpers reutilizáveis
- What: Criar `src/utils/validators.py` (validar `nome_cidade`, `sigla_uf`), `src/utils/normalizers.py` (trim, remoção de múltiplos espaços, unicode normalize) e `src/utils/http_client.py` (wrapper de httpx.AsyncClient com timeouts/retries padrão).
- Where:
  - `src/utils/validators.py`
  - `src/utils/normalizers.py`
  - `src/utils/http_client.py`
- Depends on: T02
- Reuses: —
- Done when:
  - Validators retornam booleans/raises adequados; normalizers produzem strings previsíveis.
- Tests:
  - `tests/test_utils_validators.py`, `tests/test_utils_normalizers.py`
  - Executar: `pytest tests/test_utils_*.py -q`

---

### T14 — Testes unitários: cobertura dos serviços e repositórios
- ID: T14
- Título: Adicionar testes unitários cobrindo services e repositories
- What: Implementar testes unitários para `city_service`, `weather_service`, `history_service`, `series_service`, `history_repository` com mocks e DB in-memory.
- Where:
  - `tests/test_city_service.py`
  - `tests/test_weather_service.py`
  - `tests/test_history_service.py`
  - `tests/test_series_service.py`
  - `tests/test_history_repository.py`
- Depends on: T05, T06, T07, T08, T09, T10
- Reuses: `respx`/`pytest-httpx` fixtures
- Done when:
  - Cada teste unitário roda e passa localmente.
- Tests:
  - `pytest tests/ -q`

---

### T15 — Testes de integração (TestClient)
- ID: T15
- Título: Implementar testes de integração de rota com TestClient
- What: Criar testes que sobem a app com dependências sobrescritas (clients mockados, DB in-memory) e validam fluxos end‑to‑end: health → cidades → clima → historico → serie.
- Where:
  - `tests/integration/test_end_to_end.py`
- Depends on: T01, T03, T06, T11, T12
- Reuses: fixtures de override de dependências e respx
- Done when:
  - Teste end-to-end simula chamadas externas e valida respostas e persistência em histórico.
- Tests:
  - `pytest tests/integration/test_end_to_end.py -q`

---

### T16 — Documentação e exemplos (README / Postman)
- ID: T16
- Título: Atualizar README e adicionar exemplos de requests
- What: Atualizar `README.md` com instruções de dev (rodar app, executar testes) e adicionar coleção de exemplos em `.specs/examples/` (ou `docs/`) com exemplos curl/TestClient.
- Where:
  - `README.md`
  - `.specs/examples/postman_collection.json` (opcional)
- Depends on: T11, T14, T15
- Reuses: `.specs/features/api-pesquisa-clima/spec.md` para exemplos
- Done when:
  - README contém instruções claras para rodar e testar; coleção de exemplos disponível.
- Tests:
  - Revisão manual: seguir README para levantar app e executar `pytest`.

---

### T17 — Limpeza final e preparação para PR
- ID: T17
- Título: Lint, formatação e checklist de PR
- What: Rodar linters/formatters configurados (se houver), atualizar CHANGES/ROADMAP se necessário, verificar checklists em `docs/checklists.md`.
- Where:
  - repositório raiz (`pyproject.toml` / config de linter se existir)
- Depends on: T01..T16
- Reuses: `docs/checklists.md`
- Done when:
  - Código formatado, testes passam e PR checklist preenchido.
- Tests:
  - `pytest -q` e comandos de lint (ex.: `ruff`, `black`) se aplicáveis.

---

Observação: as tasks acima foram escritas para produzir commits pequenos e revisões independentes. Posso quebrar qualquer tarefa maior em subtasks ainda mais atômicas (ex.: separar criação de arquivo de rota e wiring em `main.py`) se desejar maior granularidade.
