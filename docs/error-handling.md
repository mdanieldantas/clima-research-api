# error handling – api de pesquisa em clima

este documento define como erros devem ser representados em json, quais códigos http usar e como configurar exceptions e handlers globais.

## 1. objetivos

- nunca retornar html padrão do fastapi/starlette.
- garantir um formato consistente de erro em toda a api.
- separar responsabilidades:
  - rotas lançam exceções (400, 404, 503).
  - handlers globais convertem exceções em respostas json.
  - schemas definem o formato do payload de erro.

## 2. schema de erro

local esperado do schema:

- arquivo: `src/schemas/error.py`
- nome sugerido: `errorresponse`

campos recomendados (novo formato padronizado):

```python
from pydantic import BaseModel
from typing import Optional, Any

class ErrorResponse(BaseModel):
  status: int                 # status HTTP (ex.: 400, 404, 503)
  error_code: str             # código de erro interno, ex.: "INVALID_INPUT", "CITY_NOT_FOUND"
  message: str                # mensagem curta, amigável, em português
  details: Optional[Any] = None  # opcional: infos adicionais (lista de erros de campo, etc.)
```

Observação: o campo `status` representa o código HTTP retornado; `error_code` é um identificador interno que ajuda clientes e logs a identificar o tipo de erro sem depender apenas do status HTTP.

## 3. códigos http e códigos internos

### 3.1 http status

- `400 bad request`
  - entrada inválida (ex.: nome de cidade com menos de 2 caracteres, sigla_uf com formato errado).
- `404 not found`
  - cidade ou uf não encontrada nas apis externas ou no histórico.
- `503 service unavailable`
  - falha em serviços externos (apis de cidade/clima) ou indisponibilidade do banco.

### 3.2 códigos internos (`error_code`)

exemplos sugeridos:

- `INVALID_INPUT` – entradas inválidas em geral.
- `CITY_NOT_FOUND` – cidade não encontrada.
- `STATE_NOT_FOUND` – uf não encontrada.
- `HISTORY_NOT_FOUND` – não há histórico para a cidade (para endpoints de recurso único; para listas, preferir 200 + array vazio).
- `EXTERNAL_SERVICE_ERROR` – erro ao chamar API externa (ibge, brasil-api, open-meteo).
- `DATABASE_ERROR` – erro ao acessar o banco.

A `message` deve ser curta e clara, em português, ex.: "cidade não encontrada". O `status` deve conter o HTTP code correspondente (ex.: 404).

## 4. exceptions de domínio

local recomendado:

- arquivo: `src/core/exceptions.py`

exemplos de exceções personalizadas:

```python
class InvalidInputError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details

class NotFoundError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details

class ExternalServiceError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details
```

as rotas e serviços devem levantar essas exceções em vez de retornar dicionários manualmente.

## 5. handlers globais

local esperado:

- arquivo: `src/core/handlers.py`

os handlers devem registrar funções no fastapi para cada exceção relevante e para erros genéricos.

exemplo de mapeamento:

 - `invalidinputerror` → http 400 + `error_code="INVALID_INPUT"`.
 - `notfounderror` → http 404 + `error_code` específico (`CITY_NOT_FOUND`, `STATE_NOT_FOUND`).
 - `externalserviceerror` → http 503 + `error_code="EXTERNAL_SERVICE_ERROR"`.
 - exceções não tratadas (`exception`) → http 500 com um `error_code` genérico (`"INTERNAL_ERROR"`), evitando vazar detalhes sensíveis.

Cada handler deve retornar um `ErrorResponse` como JSON, garantindo que o `status` HTTP da resposta corresponda ao campo `status` no payload.

## 6. integração com a aplicação (main.py)

em `src/main.py`, a aplicação deve:

- criar a instância `fastapi`.
- registrar os handlers globais de erro (funções definidas em `src/core/handlers.py`).
- garantir que exceções levantadas em rotas/serviços sejam interceptadas e convertidas em `errorresponse`.

formatos de resposta de erro **devem ser consistentes** em todos os endpoints.

## 7. uso em rotas e serviços

padrão esperado:

- validações em rotas e serviços:
  - se entrada inválida → `raise InvalidInputError(...)`.
  - se recurso não encontrado → `raise NotFoundError(...)`.
  - se api externa falhou → `raise ExternalServiceError(...)`.

- rotas não devem construir respostas de erro manualmente; apenas levantam as exceções corretas.
- serviços também podem levantar exceções, que serão tratadas pelos handlers globais.

## 8. testes de erro

para cada rota, deve haver testes cobrindo:

- cenários de 400, 404, 503.
 - verificação de que:
  - o status code é o esperado.
  - a estrutura do json corresponde a `ErrorResponse` (campos: `status`, `error_code`, `message`, `details`).
  - o campo `error_code` é o apropriado para o cenário (ex.: `"INVALID_INPUT"`, `"CITY_NOT_FOUND"`).

detalhes adicionais sobre arquitetura geral estão em `architecture-rules.md`; padrões de rotas em `docs/routes-guidelines.md`.