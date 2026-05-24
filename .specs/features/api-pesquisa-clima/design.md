# Design: api-pesquisa-clima

Referências principais:
- Especificação de requisitos: [.specs/features/api-pesquisa-clima/spec.md](.specs/features/api-pesquisa-clima/spec.md)
- Persistência: [docs/persistence-guidelines.md](docs/persistence-guidelines.md)
- Rotas & responsabilidades: [docs/routes-guidelines.md](docs/routes-guidelines.md)
- Tratamento de erro: [docs/error-handling.md](docs/error-handling.md)
- Padrões de teste: [docs/testing-guidelines.md](docs/testing-guidelines.md)

## Resumo
- Objetivo: API REST para consulta de clima por nome de cidade, resolução geográfica via IBGE/Brasil API, consulta Open‑Meteo, persistência em `query_history` e endpoints de histórico/serie temporal. Seguir camadas: rotas → services → repositories → models/schemas → utilitários.

## Arquitetura em camadas (visão geral)
- `src/api/routes/*` — pontas HTTP (APIRouter). Ver [docs/routes-guidelines.md](docs/routes-guidelines.md). Rotas: `health`, `clima`, `cidades`, `historico`, `serie`.
- `src/services/*` — lógica de negócio (orquestra: resolver cidade → consultar clima → persistir → retornar).
  - `city_service` — resolver cidade (IBGE primário, Brasil API fallback), normalização.
  - `weather_service` — consulta Open‑Meteo, normalização do payload.
  - `history_service` — gravação e leitura de `query_history`.
  - `series_service` — agregações (min/max/avg) e série temporal.
- `src/repositories/*` — encapsula acesso a banco (SQLAlchemy). Ex.: `history_repository.save_query(...)`, `history_repository.list_by_city(...)`, `history_repository.agg_series_by_city(...)`.
- `src/models/*` — modelos SQLAlchemy. Arquivo principal: `src/models/query_history.py` (conforme [docs/persistence-guidelines.md](docs/persistence-guidelines.md)).
- `src/schemas/*` — Pydantic: `ClimaResponse`, `CidadeResponse`, `HistoricoItem`, `SerieResponse`, `ErrorResponse`.
- `src/core/*` — `database.py`, `config.py`, `exceptions.py`, `handlers.py` (erro global).
- `src/utils/*` — validações (`validators.py`), normalização de strings, helpers de tempo (UTC), cliente HTTP (httpx wrapper com timeouts/retries).

## Fluxos principais (passo-a-passo)

### 1) Consulta de clima (`GET /api/v1/clima/{nome_cidade}`)
- Rota valida `nome_cidade` (mínimo 2 chars) via `validators`.
- `CityService.resolve(nome_cidade)`:
  - Trim, normaliza case/acentos.
  - Chamar IBGE Localidades (primary). Se 404/erro de rede, tentar Brasil API (fallback).
  - Resultado: `{city_name, state_code, latitude, longitude, source_city_api}`.
  - Se não encontrado → raise `NotFoundError("Cidade não encontrada", details=...)`.
- `WeatherService.fetch(lat, lon)` (async):
  - Chamar Open‑Meteo com timeout e retry limitado; mapear para `{temperature, temperature_min, temperature_max, weather_summary, source_weather_api}`.
  - Em erro externo → raise `ExternalServiceError`.
- Persistência:
  - `HistoryService.save_query(session, combined_payload)` → salva em `query_history` (ver [docs/persistence-guidelines.md](docs/persistence-guidelines.md)).
  - Garantir `queried_at` em UTC.
- Resposta: `ClimaResponse` + metadata (apenas os campos definidos em contratos).

### 2) Listar cidades por UF (`GET /api/v1/cidades/{sigla_uf}`)
- Normalizar `sigla_uf` → maiúscula.
- Chamar IBGE (municípios por UF); fallback Brasil API se IBGE indisponível.
- Retornar `list[CidadeResponse]`.

### 3) Histórico (`GET /api/v1/historico/{nome_cidade}`)
- Validar `nome_cidade`.
- `HistoryService.list_by_city(nome_cidade)` → retorna lista ordenada `queried_at` desc.
- Se vazio → retornar `[]` com 200 (conforme spec).

### 4) Série temporal / agregações (`GET /api/v1/serie/{nome_cidade}`)
- Validar `nome_cidade`.
- `HistoryService.list_by_city` → `SeriesService.aggregate(records)`:
  - calcular `quantidade_consultas`, `temperatura_media`, `temperatura_minima`, `temperatura_maxima`, `ultimo_consultado_em`, `intervalo_datas`.
- Retornar `SerieResponse`.

## Tratamento de erros e contrato de erro
- Formato padronizado (conforme [docs/error-handling.md](docs/error-handling.md)):
  - Payload JSON: `status` (HTTP code), `error_code` (string), `message` (pt-BR), `details` (opcional).
- Exceções de domínio (arquivo: `src/core/exceptions.py`):
  - `InvalidInputError` → 400 / `INVALID_INPUT`
  - `NotFoundError` → 404 / `CITY_NOT_FOUND` or `STATE_NOT_FOUND`
  - `ExternalServiceError` → 503 / `EXTERNAL_SERVICE_ERROR`
  - `DatabaseError` → 503 / `DATABASE_ERROR`
- Handlers globais em `src/core/handlers.py` convertem exceções para `ErrorResponse` e garantem que `status` HTTP corresponda ao campo `status` no payload.

### Exemplo de payload de erro
```json
{
  "status": 404,
  "error_code": "CITY_NOT_FOUND",
  "message": "Cidade não encontrada",
  "details": "busca IBGE e Brasil API retornaram sem resultados"
}
```

## Contratos esperados (schemas principais — campos e tipos)
- `ClimaResponse` (GET /api/v1/clima/{nome_cidade})
  - `city_name`: str
  - `state_code`: str (2 letras)
  - `latitude`: float
  - `longitude`: float
  - `temperature`: float
  - `temperature_min`: float | null
  - `temperature_max`: float | null
  - `weather_summary`: str
  - `queried_at`: str (ISO 8601, UTC)
  - `source_city_api`: str (ex.: "ibge", "brasil-api")
  - `source_weather_api`: str (ex.: "open-meteo")

- `CidadeResponse` (GET /api/v1/cidades/{sigla_uf}) — lista items:
  - `city_name`: str
  - `state_code`: str
  - (opcional) `ibge_id`: int

- `HistoricoItem` (elemento de `GET /api/v1/historico/{nome_cidade}`)
  - todos campos de `ClimaResponse` exceto `source_*` podem permanecer; incluir `id` (int) e `queried_at`.

- `SerieResponse`
  - `city_name`: str
  - `quantidade_consultas`: int
  - `temperature_media`: float | null
  - `temperature_minima`: float | null
  - `temperature_maxima`: float | null
  - `ultimo_consultado_em`: str | null
  - `intervalo_datas`: { `inicio`: str | null, `fim`: str | null }

- `ErrorResponse`:
  - `status`: int
  - `error_code`: str
  - `message`: str
  - `details`: optional

## Persistência (modelo `query_history`) — campos obrigatórios
- `id` (int PK autoincrement)
- `city_name` (str)
- `state_code` (str, 2)
- `latitude` (float)
- `longitude` (float)
- `weather_summary` (str)
- `temperature` (float)
- `temperature_min` (float)
- `temperature_max` (float)
- `queried_at` (datetime UTC)
- `source_city_api` (str)
- `source_weather_api` (str)

## Pontos de decisão / Assunções
- Chamadas HTTP devem ser `async` (usar `httpx.AsyncClient`) para escalabilidade e compatibilidade com FastAPI async handlers.
- IBGE é fonte autoritativa; Brasil API é fallback em caso de indisponibilidade.
- Sem cache de coordenadas em v1 (especificação exige resolução dinâmica). Cache é enhancement para v2.
- Persistir cada consulta independentemente (mesmo que duplicada <1s), conforme spec.
- Data/hora em UTC sempre; respostas ISO 8601.
- Commit do DB: repositório faz `commit()` para operações simples; serviços deverão criar/fornecer sessão via dependência FastAPI, conforme [docs/persistence-guidelines.md](docs/persistence-guidelines.md).

## Riscos e mitigação
- Risco: APIs externas instáveis (IBGE, Brasil API, Open‑Meteo)
  - Mitigação: timeouts curtos, retries exponenciais limitados, fallback (IBGE → Brasil API), retornar 503 com `EXTERNAL_SERVICE_ERROR` e message amigável; instrumentação/metrics + alertas.
- Risco: resposta externa com schema inesperado
  - Mitigação: robusta normalização + validação; fallbacks; testes de contrato (mock com respostas adversas).
- Risco: crescimento grande de `query_history` (performance)
  - Mitigação: indexes (city_name + queried_at), paginação futura, migrar para Postgres (já planejado).
- Risco: desnormalização de nomes (acentos/case)
  - Mitigação: normalização e teste de casos com acentos/whitespace; usar correspondência exata fornecida pela API IBGE quando possível.
- Risco: inconsistências de commit/rollback
  - Mitigação: usar context manager de sessão, testes para falhas durante gravação.

## Estratégia de testes (unitário e integração)
- Unitários (pytest):
  - Services: mockar clientes HTTP (usar `respx` ou `pytest-httpx`) e testar lógica de `city_service`, `weather_service`, `series_service` isoladamente.
  - Repositories: testar com SQLite in-memory (ver [docs/persistence-guidelines.md](docs/persistence-guidelines.md)) para `save_query`, `list_by_city`, ordenação, agregações.
  - Utils: validators, normalização.
  - Cobertura de erros: 400, 404, 503 com estrutura `ErrorResponse`.
- Integração:
  - TestClient (FastAPI) para contratos de rota (`tests/test_clima.py`, `tests/test_cidades.py`, `tests/test_historico.py`, `tests/test_serie.py`, `tests/test_health.py`).
  - Substituir dependências externas por fixtures que usam `respx`/stubs; usar DB de testes (SQLite temporário) e override de dependências para `database.session`.
  - Testes end-to-end locais: executar app com TestClient, validar fluxo completo (resolve cidade → open‑meteo → persist → histórico/serie).
- Ferramentas sugeridas: `pytest`, `httpx`, `respx`/`pytest-httpx`, `factory-boy` (se precisar gerar dados), `vcr.py` opcional para registrar respostas.

## Critérios de aceitação do design (checks rápidos)
- Rotas finas que delegam para serviços (ver [docs/routes-guidelines.md](docs/routes-guidelines.md)).
- Schema de erro `ErrorResponse` implementado e usado por handlers (ver [docs/error-handling.md](docs/error-handling.md)).
- Modelo `query_history` e repositório com operações CRUD mínimas (ver [docs/persistence-guidelines.md](docs/persistence-guidelines.md)).
- Testes unitários cobrindo happy path + 1 erro por endpoint.
- Documentação mínima: README e collection Postman (ex.: `docs/` ou `.specs/`).

## Passos de implementação (TLC: Design → Tasks → Execute)
### Design (deliverables de design)
1. Definir e commitar `src/schemas/*.py` com `ClimaResponse`, `CidadeResponse`, `HistoricoItem`, `SerieResponse`, `ErrorResponse`.
   - Aceitação: pydantic models pass a validação unitária.

2. Especificar contratos das APIs externas (ex.: shape IBGE, Brasil API, Open‑Meteo) em `.specs/external_apis.md`.
   - Aceitação: exemplos de request/response com campos extraídos.

3. Esboçar handlers de erro em `src/core/handlers.py` e exceções em `src/core/exceptions.py`.
   - Aceitação: mapeamento 400/404/503 definido.

### Tasks (tarefas de implementação atômicas)
1. Criar modelos SQLAlchemy:
   - `src/models/query_history.py` com campos obrigatórios.
   - AC: migrate-less test usando SQLite in-memory persiste registro.

2. Implementar `src/core/database.py` e `src/core/config.py`:
   - Engine/session factory, url por env var, padrão sqlite.
   - AC: script de inicialização conecta sem erro.

3. Implementar repositório:
   - `src/repositories/history_repository.py` com `save_query`, `list_by_city`, `agg_series_by_city`.
   - AC: testes unitários validam insert e queries.

4. Implementar clientes HTTP (wrappers):
   - `src/clients/ibge_client.py`, `src/clients/brasil_api_client.py`, `src/clients/open_meteo_client.py` (async, timeouts, retries).
   - AC: clients têm funções testáveis e simuláveis.

5. Implementar serviços:
   - `src/services/city_service.py` (resolve com fallback).
   - `src/services/weather_service.py` (consulta Open‑Meteo e mapeia).
   - `src/services/history_service.py` (salva e lista).
   - `src/services/series_service.py` (agregação).
   - AC: testes unitários com mocks dos clients.

6. Implementar rotas (APIRouter):
   - `src/api/routes/health.py`, `clima.py`, `cidades.py`, `historico.py`, `serie.py` conforme [docs/routes-guidelines.md](docs/routes-guidelines.md).
   - AC: cada rota declara `response_model`.

7. Implementar handlers globais de erro e registrar em `src/main.py`.
   - AC: raising exceptions retorna JSON padronizado.

8. Implementar validações utilitárias:
   - `src/utils/validators.py` (nome cidade, sigla UF), `src/utils/normalizers.py`.
   - AC: testes unitários.

9. Testes:
   - Unitários para serviços, repositório, utils.
   - Integração via TestClient cobrindo todos endpoints exigidos em spec.
   - AC: pipeline local executa `pytest` com resultados esperados (happy path + um erro cada).

### Execute (verificação e entrega)
1. Rodar suíte de testes localmente (`pytest -q`). Corrigir falhas.
   - Comandos sugeridos:
     ```bash
     pytest tests/ -q
     ```

2. Criar collection de exemplos (Postman / HTTPie) em `.specs/examples/` ou `docs/README.md`.
   - AC: rotas testáveis conforme `spec.md` (ex.: `/api/v1/clima/fortaleza`).

3. Atualizar README com exemplos `curl` e instruções de dev (porta 3000).
   - AC: doc para rodar app local e executar testes.

4. Revisão de PR: revisar cobertura de testes, handlers de erro, e conformidade com `.specs/features/api-pesquisa-clima/spec.md`.

## Checklist mínimo para PR
- [ ] `src/schemas/*` implementados e importáveis.
- [ ] `src/models/query_history.py` criado.
- [ ] Repositório com testes (in-memory sqlite).
- [ ] Services com mocks passados nos testes.
- [ ] Rotas expostas em `src/api/routes/*` com `response_model`.
- [ ] Handlers de erro globais funcionando (400/404/503).
- [ ] Testes unitários e de integração adicionados a `tests/`.
- [ ] Documentação mínima atualizada (`README.md`, `.specs/examples`).

## Observações finais e próximos passos
- Esta especificação de design é suficiente para implementação por outro dev: priorizar ordem das Tasks (models → repos → services → routes → handlers → tests).
- Pós‑MVP: considerar cache de coordenadas, paginação de histórico, migração para Postgres e uso de Alembic.
- Se desejar, posso agora: (1) gerar um template de `src/schemas/clima.py` e `src/models/query_history.py` (somente documentação dos campos, sem código), ou (2) quebrar as Tasks em tickets/PRs com títulos e descrições curtas para iniciar desenvolvimento.
