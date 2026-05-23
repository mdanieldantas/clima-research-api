# guidelines de rotas – api de pesquisa em clima

estas diretrizes são para ferramentas de ia gerarem e modificarem rotas fastapi neste projeto de forma consistente.

## 1. local das rotas

- todas as rotas devem ficar em `src/api/routes/`.
- cada arquivo de rota deve agrupar endpoints do mesmo domínio:
  - `health.py` – saúde da aplicação.
  - `clima.py` – endpoints relacionados a clima.
  - `cidades.py` – endpoints relacionados a cidades/uf.
  - `historico.py` – endpoints para histórico de consultas.
  - `serie.py` – endpoints para séries temporais.

## 2. criação de routers

- cada arquivo em `src/api/routes/` deve:
  - criar um `apirouter` com:
    - prefixo começando em `/api/v1`.
    - tag coerente (ex.: `"health"`, `"clima"`, `"cidades"`).
  - expor uma variável `router` que será incluída em `main.py`.

exemplo de padrão:

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

> observação: o nome exato dos imports pode variar conforme a organização final, mas o padrão deve ser sempre: router em `src/api/routes/*` chamando serviços em `src/services/*` e schemas em `src/schemas/*`.

## 3. responsabilidade das rotas

- funções de rota devem ser **finas**:
  - validar parâmetros simples (ex.: se a string não está vazia).
  - delegar regras de negócio para serviços em `src/services/`.
  - converter entradas/saídas para schemas pydantic.
  - levantar exceções de domínio/http apropriadas (400, 404, 503).

- rotas **não** devem:
  - acessar diretamente o banco ou modelos sqlalchemy.
  - conter lógica complexa de negócio (agregações, cálculos, etc.).
  - chamar diretamente apis externas (`httpx`), isso é papel de serviços.

## 4. padrão de parâmetros e validações

- `nome_cidade`:
  - tipo: `str`.
  - regra: mínimo 2 caracteres, não pode ser string vazia.
  - invalidade → levantar erro 400.

- `sigla_uf`:
  - tipo: `str`.
  - regra: exatamente 2 letras (a–z), preferencialmente maiúsculas na normalização.
  - invalidade → levantar erro 400.

- sempre que possível, usar funções de validação em `src/utils/validators.py` para evitar duplicação de lógica.

## 5. schemas e tipos de resposta

- toda rota deve declarar explicitamente `response_model` com um schema pydantic localizado em `src/schemas/`.
- para rotas de lista (ex.: `/cidades/{sigla_uf}`), usar listas tipadas, ex.: `list[CidadeResponse]`.
- respostas de erro nunca devem ser html; devem usar o schema de erro definido em `schemas/error.py` e os handlers globais (ver `docs/error-handling.md`).

## 6. códigos de status esperados

- `get /api/v1/health`
  - 200 em caso de sucesso.

- `get /api/v1/clima/{nome_cidade}`
  - 200 em caso de sucesso (dados de clima + metadados).
  - 400 se `nome_cidade` inválido.
  - 404 se a cidade não for encontrada.
  - 503 se a api de cidades ou a api de clima estiver indisponível.

- `get /api/v1/cidades/{sigla_uf}`
  - 200 com lista de cidades da uf.
  - 400 se `sigla_uf` inválida.
  - 404 se a uf não for encontrada.
  - 503 se a api externa estiver indisponível.

- `get /api/v1/historico/{nome_cidade}` e `/serie/{nome_cidade}`
  - 200 com histórico ou série.
  - 400 se `nome_cidade` inválido.
  - 404 se não houver registros para a cidade.
  - 503 se houver falha no acesso ao banco ou serviço dependente.

## 7. integração com serviços

- rotas devem injetar serviços via `depends` quando fizer sentido, ex.:

```python
@router.get("/{nome_cidade}", response_model=ClimaResponse)
async def get_clima(
    nome_cidade: str,
    weather_service: WeatherService = Depends(),
    history_service: HistoryService = Depends(),
):
    ...
```

- a lógica de:
  - resolver coordenadas,
  - chamar open-meteo,
  - salvar histórico,
  - preparar dados para série temporal,

deve ficar nos serviços, não na rota.

## 8. convenções de nomes

- nomes de funções de rota:
  - usar verbos claros: `get_clima`, `list_cidades`, `get_historico`, `get_serie`.
- nomes de parâmetros de caminho devem ser descritivos:
  - `{nome_cidade}`, `{sigla_uf}`, e não `{id}` genérico.
- nomes das tags em `apirouter` devem ser curtos e coerentes com o domínio do arquivo.

## 9. testes de rota

- cada rota nova ou modificada deve ter testes em `tests/`:
  - usar `testclient` do fastapi.
  - garantir que:
    - status codes esperados são retornados.
    - o payload corresponde ao schema.
    - erros (400, 404, 503) retornam json padronizado.

para detalhes mais gerais de arquitetura, consultar `architecture-rules.md`.