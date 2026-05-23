## Prompts para usar com Copilot (VS Code)

Use estes prompts no chat do Copilot, sempre abrindo junto os arquivos:
- `architecture-rules.md`
- `docs/routes-guidelines.md`
- `docs/error-handling.md`
- `docs/persistence-guidelines.md`
- `docs/testing-guidelines.md`
[file:6]

---

### 1) Criar base da API (main.py + CORS + porta 3000)

Quero iniciar a API de Pesquisa em Clima seguindo as especificações de `architecture-rules.md`.

Tarefas:
- Criar `src/main.py` com:
  - instância FastAPI
  - configuração de CORS liberando acesso padrão para testes (localhost)
  - configuração para rodar na porta 3000
  - registro de routers, mesmo que ainda só exista o de health
- Criar estrutura mínima de pastas em `src/core/` com arquivos vazios ou esqueleto:
  - `config.py`
  - `database.py`
  - `exceptions.py`
  - `handlers.py`

Regras:
- Siga estritamente as convenções descritas em `architecture-rules.md`.
- Não crie outras rotas além do esqueleto de health.
- Mostre apenas o conteúdo final dos arquivos criados/alterados, em blocos separados.

---

### 2) Criar endpoint GET /api/v1/health + teste

Usando `architecture-rules.md`, `docs/routes-guidelines.md` e `docs/testing-guidelines.md`, implemente o endpoint de health.

Tarefas:
- Criar `src/api/routes/health.py` com:
  - `APIRouter` com prefixo `/api/v1/health` e tag `"health"`.
  - endpoint `GET /api/v1/health` que responde JSON com:
    - `status`: `"ok"`
    - `service`: nome da API
    - `timestamp`: string datetime em formato ISO 8601
- Criar `src/schemas/health.py` com o schema Pydantic correspondente à resposta.
- Registrar o router de health em `src/main.py`.
- Criar `tests/test_health.py` seguindo `docs/testing-guidelines.md`:
  - testar status code 200
  - testar campos `status` e `service`
  - garantir que a resposta é JSON válido

Regras:
- Rotas e schemas devem seguir `docs/routes-guidelines.md`.
- Testes devem seguir `docs/testing-guidelines.md`.
- Mostre o conteúdo completo dos arquivos criados/alterados.

---

### 3) Criar schema de erro, exceptions e handlers globais

Usando `architecture-rules.md` e `docs/error-handling.md`, implemente a infraestrutura de erros padronizados.

Tarefas:
- Criar `src/schemas/error.py` com o schema `ErrorResponse` exatamente como especificado em `docs/error-handling.md`.
- Criar `src/core/exceptions.py` com as exceptions:
  - `InvalidInputError`
  - `NotFoundError`
  - `ExternalServiceError`
- Criar `src/core/handlers.py` com handlers FastAPI que:
  - mapeiem `InvalidInputError` → HTTP 400 com `code="INVALID_INPUT"`.
  - mapeiem `NotFoundError` → HTTP 404 com `code` apropriado (passado na exceção ou definido no handler).
  - mapeiem `ExternalServiceError` → HTTP 503 com `code="EXTERNAL_SERVICE_ERROR"`.
  - tratem exceções genéricas (`Exception`) como HTTP 500 com `code="INTERNAL_ERROR"`.
- Registrar os handlers globais em `src/main.py`.

Regras:
- Sempre retornar JSON usando `ErrorResponse`.
- Não retornar HTML padrão do FastAPI.
- Seguir exatamente o contrato descrito em `docs/error-handling.md`.

Saída:
- Mostre os arquivos completos: `src/schemas/error.py`, `src/core/exceptions.py`, `src/core/handlers.py` e as mudanças em `src/main.py`.

---

### 4) Criar modelo query_history + database + repositório

Usando `architecture-rules.md` e `docs/persistence-guidelines.md`, implemente a camada de persistência básica.

Tarefas:
- Implementar `src/core/database.py` com:
  - criação do `engine` SQLAlchemy para SQLite
  - `SessionLocal` (sessionmaker)
  - função utilitária para obter sessão (padrão de dependência para FastAPI, se fizer sentido)
- Implementar `src/models/query_history.py` com o modelo SQLAlchemy conforme especificação de campos em `docs/persistence-guidelines.md`.
- Implementar `src/repositories/history_repository.py` com funções:
  - `save_query_history(...)` para salvar um novo registro
  - `list_history_by_city(city_name: str)` para buscar histórico por cidade
  - (opcional) função para obter registros em ordem temporal para séries

Regras:
- Não acessar o banco diretamente nas rotas.
- Pensar na futura migração para PostgreSQL, seguindo os tipos sugeridos.
- Seguir estritamente o que está em `docs/persistence-guidelines.md`.

Saída:
- Mostre o conteúdo completo dos arquivos criados/alterados.

---

### 5) Criar endpoints de cidades (GET /api/v1/cidades/{sigla_uf}) + testes

Usando `architecture-rules.md`, `docs/routes-guidelines.md`, `docs/error-handling.md` e `docs/testing-guidelines.md`, implemente o fluxo de cidades.

Tarefas:
- Criar `src/services/city_service.py` que:
  - valide `sigla_uf` usando utilitários em `src/utils/validators.py` (crie se necessário).
  - consulte uma API pública (IBGE ou Brasil API) para listar cidades de uma UF.
  - em caso de erro de entrada → lançar `InvalidInputError`.
  - em caso de UF não encontrada → lançar `NotFoundError`.
  - em caso de falha de API externa → lançar `ExternalServiceError`.
- Criar `src/schemas/cidade.py` com os schemas de resposta para lista de cidades.
- Criar `src/api/routes/cidades.py` com:
  - rota `GET /api/v1/cidades/{sigla_uf}` seguindo `docs/routes-guidelines.md`.
- Criar `tests/test_cidades.py` com testes:
  - cenário 200 (UF válida, lista de cidades).
  - cenário 400 (UF inválida).
  - cenário 404 (UF não encontrada).
  - cenário 503 (falha simulada na API externa).

Regras:
- Rotas finas, serviços com a lógica.
- Erros sempre em JSON usando `ErrorResponse`.
- Testes seguindo `docs/testing-guidelines.md`.

Saída:
- Mostre os arquivos completos criados/alterados.

---

### 6) Criar endpoint de clima (GET /api/v1/clima/{nome_cidade}) + histórico

Usando todos os documentos (`architecture-rules.md`, `docs/routes-guidelines.md`, `docs/error-handling.md`, `docs/persistence-guidelines.md`, `docs/testing-guidelines.md`), implemente o fluxo de clima com persistência de histórico.

Tarefas:
- Criar/ajustar `src/services/weather_service.py` para:
  - receber um `nome_cidade`.
  - resolver cidade + coordenadas chamando o `CityService` (ou equivalente).
  - consultar Open-Meteo usando latitude/longitude (sem coordenadas fixas em código).
  - montar um objeto de domínio com dados de clima (temp, min, max, summary).
  - chamar o repositório `history_repository` para salvar um registro em `query_history`.
- Criar/ajustar `src/services/history_service.py` com:
  - funções para buscar histórico por cidade usando o repositório.
- Criar `src/schemas/clima.py` com o schema de resposta para o endpoint de clima.
- Criar/ajustar `src/api/routes/clima.py` com:
  - `GET /api/v1/clima/{nome_cidade}` seguindo padrões de validação, erro e uso de serviços.
- Criar/ajustar `tests/test_clima.py` cobrindo:
  - cenário 200 (clima encontrado, histórico salvo).
  - cenário 400 (nome_cidade inválido).
  - cenário 404 (cidade não encontrada).
  - cenário 503 (falha em API externa).

Regras:
- Não hardcodar latitude/longitude.
- Persistir toda consulta bem-sucedida em `query_history`.
- Usar exceptions/handlers padronizados para erros.

Saída:
- Mostre o conteúdo completo dos arquivos criados/alterados.

---

### 7) Criar endpoints de histórico e série temporal + testes

Usando os mesmos documentos de arquitetura, rotas, erros, persistência e testes, implemente os endpoints de histórico e série.

Tarefas:
- Criar/ajustar `src/services/history_service.py` e `src/services/series_service.py` com:
  - funções para buscar histórico por cidade.
  - funções para montar série temporal (lista de pontos com `queried_at`, `temperature`, etc.).
- Criar/ajustar `src/schemas/historico.py` e `src/schemas/serie.py`.
- Criar `src/api/routes/historico.py` e `src/api/routes/serie.py` com:
  - `GET /api/v1/historico/{nome_cidade}`
  - `GET /api/v1/serie/{nome_cidade}`
  seguindo os padrões de `docs/routes-guidelines.md`.
- Criar/ajustar `tests/test_historico.py` e `tests/test_serie.py` cobrindo:
  - cenário 200 com dados.
  - cenário 404 quando não houver registros para a cidade.
  - cenários de erro de entrada e erro de serviço, se aplicável.

Regras:
- Lógica de agregação deve ficar nos serviços.
- Rotas apenas orquestram schemas, serviços e erros.

Saída:
- Mostre o conteúdo completo dos arquivos criados/alterados.