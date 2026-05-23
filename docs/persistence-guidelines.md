# persistence guidelines – api de pesquisa em clima

estas diretrizes definem como a persistência deve funcionar neste projeto, com foco no modelo `query_history` e na transição futura de sqlite para postgresql.

## 1. objetivos

- registrar o histórico de consultas de clima em uma tabela única (`query_history`).
- permitir auditoria, reuso e análises temporais.
- isolar acesso a banco em repositórios (sqlalchemy), sem lógica de negócio.
- facilitar migração futura de sqlite para postgresql com o mínimo de retrabalho.

## 2. modelo principal: query_history

local esperado:

- arquivo: `src/models/query_history.py`
- tecnologia: sqlalchemy (declarative base)

campos obrigatórios:

- `id` – chave primária (inteiro, autoincremento).
- `city_name` – nome da cidade consultada.
- `state_code` – sigla da uf (2 letras).
- `latitude` – latitude usada na consulta.
- `longitude` – longitude usada na consulta.
- `weather_summary` – resumo textual do clima (ex.: “céu limpo”, “chuva leve”).
- `temperature` – temperatura atual (número).
- `temperature_min` – temperatura mínima no período.
- `temperature_max` – temperatura máxima no período.
- `queried_at` – data/hora da consulta (idealmente armazenada em utc).
- `source_city_api` – identificação da api usada para cidade (ex.: “ibge”, “brasil-api”).
- `source_weather_api` – identificação da api usada para clima (ex.: “open-meteo”).

regra: **toda consulta bem-sucedida de clima deve gerar um registro em `query_history`**.

## 3. banco de dados

- banco atual: `sqlite` (arquivo local).  
- banco alvo futuro: `postgresql`.

regras:

- não usar recursos muito específicos de sqlite (tipos exóticos, funções especiais).
- manter tipos compatíveis com postgresql (inteiros, textos, floats, timestamps).
- toda configuração de engine/session deve ficar em `src/core/database.py`.

## 4. organização de código

- `src/core/database.py`
  - cria o `engine` sqlalchemy.
  - expõe uma fábrica de sessões (ex.: `sessionmaker`).
  - configurações de url de banco vêm de `config`/variáveis de ambiente.

- `src/models/query_history.py`
  - define o modelo sqlalchemy com a tabela `query_history`.

- `src/repositories/history_repository.py`
  - encapsula operações de banco relacionadas a histórico:
    - salvar nova consulta (`save_query` / `save_query_history`).
    - buscar histórico por cidade (`list_by_city`).
    - buscar série temporal (`list_series_by_city` ou similar).

serviços (`src/services/history_service.py`, `src/services/series_service.py`) devem chamar o repositório, não o modelo diretamente.

## 5. padrões de uso de sessão

- preferir padrões explícitos de sessão, por exemplo:

  - criar a sessão no serviço ou via dependência do fastapi.
  - passar a sessão para o repositório quando necessário.
  - garantir fechamento/rollback apropriado (context manager ou dependências).

- evitar sessões globais compartilhadas de forma não controlada.

## 6. registros de histórico

para cada consulta bem-sucedida ao endpoint `GET /api/v1/clima/{nome_cidade}`:

- os dados a serem persistidos devem vir:
  - do serviço de cidades (nome normalizado, `state_code`, `latitude`, `longitude`).
  - do serviço de clima (temperaturas, resumo, fonte da api).

- o repositório deve:
  - criar uma instância de `query_history`.
  - preencher todos os campos obrigatórios.
  - persistir a entidade na sessão e fazer commit (ou delegar o commit, conforme o padrão adotado no projeto).

## 7. consultas de histórico e séries

para endpoints de histórico/série:

- `GET /api/v1/historico/{nome_cidade}`:
  - deve retornar a lista de registros `query_history` daquela cidade, ordenados por `queried_at` (asc ou desc, mas padronizar).
  - a conversão para schemas de resposta fica no serviço/rota.

- `GET /api/v1/serie/{nome_cidade}`:
  - deve usar os registros de `query_history` para construir uma série temporal (ex.: lista de pontos com `queried_at`, `temperature`, `temperature_min`, `temperature_max`).
  - agregações simples (média, máximos, mínimos) podem ser feitas no serviço, com base nos dados retornados pelo repositório.

## 8. migração futura para postgresql

para facilitar a migração:

- centralizar a url do banco (sqlite/postgres) em configurações (`src/core/config.py`).
- evitar espalhar strings de conexão pelo código.
- usar somente tipos de coluna padrão (integer, string/text, float, datetime).
- se possível, estruturar o projeto pensando em uso de migrations (alembic ou similar), mesmo que não seja implementado de imediato.

quando for migrar:

- ajustar apenas url e configurações de engine.
- se usar migrations, gerar as migrations para postgresql.
- garantir que `query_history` esteja compatível (tipos e constraints).

## 9. testes relacionados à persistência

- testar repositórios isoladamente, usando sqlite em memória quando possível.
- garantir que:
  - um registro é criado corretamente ao salvar consulta.
  - consultas por cidade retornam os registros esperados.
  - a ordenação temporal funciona como esperado.
  - casos sem histórico retornam vazio (ou geram `notfounderror` em nível de serviço, conforme design definido).

para visão geral de arquitetura, consultar `architecture-rules.md`. para padrões de rotas e erros, ver `docs/routes-guidelines.md` e `docs/error-handling.md`.