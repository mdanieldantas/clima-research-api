# Plano de Construção — API de Pesquisa em Clima

## 1. Objetivo do projeto

Construir uma API REST em Python para pesquisa em clima, com foco em agregação de dados geográficos e meteorológicos, persistência de histórico e apoio a séries temporais.  
O projeto será desenvolvido para portfólio técnico e para demonstrar aderência temática a iniciativas de pesquisa em clima e meio ambiente, com linguagem e apresentação compatíveis com um perfil profissional para seleção FUNCEME [web:7][web:13].

## 2. Proposta técnica

A aplicação deve receber o nome de uma cidade e resolver dinamicamente seus dados geográficos e climáticos por meio de APIs públicas.  
A solução não deve usar coordenadas fixas em código, deve devolver somente JSON e deve armazenar consultas para permitir histórico e análises posteriores [file:5].

## 3. Escopo funcional

### Endpoints principais
- `GET /api/v1/health`
- `GET /api/v1/clima/{nome_cidade}`
- `GET /api/v1/cidades/{sigla_uf}`

### Endpoints de apoio
- `GET /api/v1/historico/{nome_cidade}`
- `GET /api/v1/serie/{nome_cidade}`

### Funcionalidades esperadas
- Buscar cidade por nome.
- Buscar lista de cidades por UF.
- Consultar clima com base em latitude e longitude obtidas dinamicamente.
- Registrar histórico das consultas.
- Gerar visão temporal das consultas armazenadas.
- Padronizar erros em JSON.
- Habilitar CORS e rodar na porta 3000 [file:5].

## 4. Requisitos de arquitetura

- Linguagem: Python.
- Framework sugerido: FastAPI.
- Cliente HTTP: httpx.
- Banco de dados: SQLite no início, com possibilidade de migração para PostgreSQL.
- Persistência: SQLAlchemy.
- Testes: pytest.
- Documentação: README, Postman Collection e arquivo de integrantes.
- Organização por camadas: rotas, serviços, repositórios, modelos, schemas, utilitários.

## 5. Estrutura de pastas

```text
README.md
INTEGRANTES.md
src/
  main.py
  core/
    config.py
    database.py
    exceptions.py
    handlers.py
  api/
    routes/
      health.py
      clima.py
      cidades.py
      historico.py
      serie.py
  schemas/
    health.py
    clima.py
    cidade.py
    historico.py
    serie.py
    error.py
  services/
    city_service.py
    weather_service.py
    history_service.py
    series_service.py
  repositories/
    history_repository.py
  models/
    query_history.py
  utils/
    validators.py
    datetime_utils.py
tests/
  test_health.py
  test_clima.py
  test_cidades.py
  test_historico.py
docs/
  postman_collection.json
```

## 6. Fluxo de execução

1. O usuário informa o nome de uma cidade.
2. A API valida a entrada.
3. O sistema busca a cidade em uma base pública.
4. O sistema obtém coordenadas atualizadas dinamicamente.
5. O sistema consulta a API climática.
6. A resposta é normalizada em JSON.
7. A consulta é salva no banco.
8. O histórico pode ser consultado depois.
9. O endpoint de série temporal consolida os registros salvos [file:5].

## 7. Modelo de dados

### Tabela `query_history`
- `id`
- `city_name`
- `state_code`
- `latitude`
- `longitude`
- `weather_summary`
- `temperature`
- `temperature_min`
- `temperature_max`
- `queried_at`
- `source_city_api`
- `source_weather_api`

### Finalidade
Essa tabela guarda o histórico das consultas para permitir auditoria, reuso e análises temporais.  
Ela também fortalece o projeto para portfólio, porque mostra persistência e tratamento de dados ambientais.

## 8. Validações e erros

### Validações obrigatórias
- Nome da cidade com pelo menos 2 caracteres.
- Sigla da UF com exatamente 2 letras.
- Resposta sempre em JSON.
- Erros não devem retornar HTML padrão do framework [file:5].

### Erros padronizados
- `400` para entrada inválida.
- `404` para cidade ou UF não encontrada.
- `503` para serviço externo indisponível [file:5].

## 9. APIs externas sugeridas

### Para cidades e estados
- IBGE Localidades.
- Brasil API.

### Para clima
- Open-Meteo.

### Observação
A consulta deve ser feita por nome da cidade e as coordenadas devem ser obtidas em tempo de execução, sem uso de valores fixos no código [file:5].  
A Open-Meteo possui suporte a clima histórico e séries temporais, o que combina bem com o objetivo do projeto [web:11][web:17][web:20].

## 10. Plano de construção por etapas

### Etapa 1 — Preparação
- Criar repositório.
- Definir nome do projeto.
- Montar estrutura de pastas.
- Criar `README.md` e `INTEGRANTES.md`.
- Definir stack Python.

### Etapa 2 — Base da API
- Criar FastAPI.
- Configurar CORS.
- Configurar porta 3000.
- Criar `GET /api/v1/health`.
- Garantir JSON em toda resposta [file:5].

### Etapa 3 — Tratamento de erros
- Criar handlers globais.
- Padronizar payload de erro.
- Testar cenários 400, 404 e 503.

### Etapa 4 — Integração geográfica
- Criar serviço de busca de cidade.
- Criar endpoint `GET /api/v1/cidades/{sigla_uf}`.
- Buscar municípios por UF.
- Validar UF e mapear resultados.

### Etapa 5 — Integração climática
- Criar serviço de clima.
- Criar endpoint `GET /api/v1/clima/{nome_cidade}`.
- Resolver latitude e longitude dinamicamente.
- Buscar dados climáticos em API pública.
- Normalizar resposta.

### Etapa 6 — Persistência
- Criar banco SQLite.
- Criar tabela de histórico.
- Salvar cada consulta climática.
- Preparar base para PostgreSQL futuro.

### Etapa 7 — Histórico e série temporal
- Criar `GET /api/v1/historico/{nome_cidade}`.
- Criar `GET /api/v1/serie/{nome_cidade}`.
- Mostrar consultas em ordem temporal.
- Gerar agregações simples, como média e máximos.

### Etapa 8 — Testes
- Criar testes de sucesso.
- Criar testes de erro.
- Cobrir health, clima e cidades.
- Cobrir histórico se houver tempo.

### Etapa 9 — Documentação final
- Completar README.
- Criar coleção Postman.
- Revisar exemplos JSON.
- Revisar nomes de módulos e funções.
- Publicar repositório.

## 11. Estratégia de portfólio

O projeto deve ser apresentado como uma **API de Pesquisa em Clima**, com ênfase em:
- integração de APIs públicas;
- persistência de consultas;
- histórico climático;
- apoio a séries temporais;
- dados geográficos e meteorológicos;
- arquitetura organizada em Python.

Essa apresentação é mais forte para currículo porque mostra backend, integração de sistemas, tratamento de dados ambientais e estrutura profissional de projeto [web:7][web:13].

## 12. Critérios de qualidade

Antes de considerar o projeto pronto:
- a API deve responder em `http://localhost:3000`;
- todos os endpoints devem devolver JSON;
- os erros devem ser previsíveis;
- não pode haver coordenadas fixas no código;
- o histórico deve ser persistido;
- os testes devem executar com sucesso;
- a documentação deve estar clara.

## 13. Entregáveis finais

- Código-fonte em Python.
- README técnico.
- Testes automatizados.
- Coleção Postman.
- Banco de dados local para histórico.
- Endpoint de série temporal.

## 14. Observação final

Se o projeto for usado para seleção e portfólio, o mais importante é reforçar a narrativa de:
- pesquisa em clima;
- integração de dados;
- persistência;
- análise temporal;
- estrutura técnica limpa.

Isso aproxima o projeto do vocabulário usado em iniciativas de pesquisa e em editais da área climática [web:7][web:13].