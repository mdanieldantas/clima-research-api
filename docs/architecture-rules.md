# Guidelines de Rotas – API de Pesquisa em Clima

Estas diretrizes são para ferramentas de IA gerarem e modificarem rotas FastAPI neste projeto de forma consistente.

## 1. Local das rotas

- Todas as rotas devem ficar em `src/api/routes/`.
- Cada arquivo de rota deve agrupar endpoints do mesmo domínio:
  - `health.py` – saúde da aplicação.
  - `clima.py` – endpoints relacionados a clima.
  - `cidades.py` – endpoints relacionados a cidades/UF.
  - `historico.py` – endpoints para histórico de consultas.
  - `serie.py` – endpoints para séries temporais.

## 2. Criação de routers

- Cada arquivo em `src/api/routes/` deve:
  - Criar um `APIRouter` com:
    - prefixo começando em `/api/v1`.
    - tag coerente (ex.: `"health"`, `"clima"`, `"cidades"`).
  - Expor uma variável `router` que será incluída em `main.py`.

Exemplo de padrão:

```python
from fastapi import APIRouter, Depends
from src.schemas.clima import ClimaResponse
from src.services.weather_service import WeatherService

router = APIRouter(
    prefix="/api/v1/clima",
    tags=["clima"],
)

@router.get("/{nome_cidade}", response_model=ClimaResponse)
async def get_clima(nome_cidade: str, service: WeatherService = Depends()):
    ...
```

> Observação: o nome exato dos imports pode variar conforme a organização final, mas o padrão deve ser sempre: router em `src/api/routes/*` chamando serviços em `src/services/*` e schemas em `src/schemas/*`.

## 3. Responsabilidade das rotas

- Funções de rota devem ser **finas**:
  - Validar parâmetros simples (ex.: se a string não está vazia).
  - Delegar regras de negócio para serviços em `src/services/`.
  - Converter entradas/saídas para schemas Pydantic.
  - Levantar exceções de domínio/HTTP apropriadas (400, 404, 503).

- Rotas **não** devem:
  - Acessar diretamente o banco ou modelos SQLAlchemy.
  - Contener lógica complexa de negócio (agregações, cálculos, etc.).
  - Chamar diretamente APIs externas (`httpx`), isso é papel de serviços.

## 4. Padrão de parâmetros e validações

- `nome_cidade`:
  - Tipo: `str`.
  - Regra: mínimo 2 caracteres, não pode ser string vazia.
  - Invalidade → levantar erro 400.

- `sigla_uf`:
  - Tipo: `str`.
  - Regra: exatamente 2 letras (A–Z), preferencialmente maiúsculas.
  - Invalidade → levantar erro 400.

- Sempre que possível, use funções de validação em `src/utils/validators.py` para evitar duplicação de lógica.

## 5. Schemas e tipos de resposta

- Toda rota deve declarar explicitamente `response_model` com um schema Pydantic localizado em `src/schemas/`.
- Para rotas de lista (ex.: `/cidades/{sigla_uf}`), usar listas tipadas, ex.: `list[CidadeResponse]`.
- Respostas de erro NUNCA devem ser HTML; devem usar o schema de erro definido em `schemas/error.py` e os handlers globais (ver `docs/ERROR_HANDLING.md`).

## 6. Códigos de status esperados

- `GET /api/v1/health`
  - 200 em caso de sucesso.

- `GET /api/v1/clima/{nome_cidade}`
  - 200 em caso de sucesso (dados de clima + metadados).
  - 400 se `nome_cidade` inválido.
  - 404 se a cidade não for encontrada.
  - 503 se a API de cidades ou a API de clima estiver indisponível.

- `GET /api/v1/cidades/{sigla_uf}`
  - 200 com lista de cidades da UF.
  - 400 se `sigla_uf` inválida.
  - 404 se a UF não for encontrada.
  - 503 se a API externa estiver indisponível.

- `GET /api/v1/historico/{nome_cidade}` e `/serie/{nome_cidade}`
  - 200 com histórico ou série.
  - 400 se `nome_cidade` inválido.
  - 404 se não houver registros para a cidade.
  - 503 se houver falha no acesso ao banco ou serviço dependente.

## 7. Integração com serviços

- Rotas devem injetar serviços via `Depends` quando fizer sentido, ex.:

```python
@router.get("/{nome_cidade}", response_model=ClimaResponse)
async def get_clima(
    nome_cidade: str,
    weather_service: WeatherService = Depends(),
    history_service: HistoryService = Depends(),
):
    ...
```

- A lógica de:
  - resolver coordenadas,
  - chamar Open‑Meteo,
  - salvar histórico,
  - preparar dados para série temporal,

deve ficar nos serviços, não na rota.

## 8. Convenções de nomes

- Nomes de funções de rota:
  - usar verbos claros: `get_clima`, `list_cidades`, `get_historico`, `get_serie`.
- Nomes de parâmetros de caminho devem ser descritivos:
  - `{nome_cidade}`, `{sigla_uf}`, e não `{id}` genérico.
- Nomes das tags em `APIRouter` devem ser curtos e coerentes com o domínio do arquivo.

## 9. Testes de rota

- Cada rota nova ou modificada deve ter testes em `tests/`:
  - usar `TestClient` do FastAPI.
  - garantir que:
    - status codes esperados são retornados.
    - o payload corresponde ao schema.
    - erros (400, 404, 503) retornam JSON padronizado.

Para detalhes mais gerais de arquitetura, consultar `ARCHITECTURE_RULES.md`.