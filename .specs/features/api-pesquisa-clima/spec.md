# API de Pesquisa em Clima — Especificação de Funcionalidade

## Declaração do Problema

Pesquisadores e profissionais de clima precisam de uma forma rápida e padronizada para consultar dados meteorológicos por nome de cidade, acessar histórico de consultas e analisar tendências temporais. Sistemas atuais exigem conhecimento prévio de coordenadas ou múltiplas chamadas a APIs espalhadas — criando fricção na pesquisa. Uma API unificada que resolva dinamicamente coordenadas por nome de cidade, persista histórico e permita análises temporais reduz essa fricção e padroniza o acesso a dados.

## Objetivos

- [ ] **API Unificada:** Usuários podem consultar clima, cidades e histórico através de uma interface RESTful única (5 endpoints, todos métodos HTTP sem POST)
  - Métrica de sucesso: Todos endpoints retornam schema JSON consistente com status codes apropriados
- [ ] **Resolução Geográfica Dinâmica:** Sistema deve resolver coordenadas de cidade no momento da requisição (sem lat/lon hardcoded no código)
  - Métrica de sucesso: Qualquer nome de cidade brasileira → coordenadas corretas (fonte autorizativa IBGE)
- [ ] **Histórico Persistente:** Cada consulta de clima é registrada com contexto completo (cidade, estado, coords, timestamp, APIs fonte)
  - Métrica de sucesso: 100% de consultas registradas, histórico recuperável e auditável
- [ ] **Pronto para Série Temporal:** Sistema suporta agregações e análise temporal de consultas passadas
  - Métrica de sucesso: Endpoint de série temporal retorna mín/máx/média precisas sobre conjunto de consultas

## Fora do Escopo

| Funcionalidade           | Razão                                                          |
| ----------------------- | ------------------------------------------------------------ |
| Autenticação/Autorização | v1 é API pública; auth adiada para v2                        |
| Streaming em tempo real  | Modelo de polling suficiente para MVP; WebSocket adiado      |
| Alertas de previsão      | Requer serviço de assinatura; fora de escopo                |
| Cálculos customizados    | API retorna dados fonte apenas; sem métricas sintéticas v1   |
| Preenchimento de dados   | Preenchimento retroativo de clima adiado para v2             |
| UI frontend              | Apenas API; UI é concern separado                            |

---

## Histórias de Usuário

### P1: Usuários podem consultar clima por nome de cidade ⭐ MVP

**História de Usuário:** Como pesquisador, quero consultar dados de clima digitando um nome de cidade para que eu obtenha condições climáticas atuais sem precisar conhecer coordenadas.

**Por que P1:** Proposta de valor central; bloqueia todas outras funcionalidades de clima; requerido para MVP demo.

**Critérios de Aceitação:**

1. QUANDO usuário chama `GET /api/v1/clima/sao-paulo` ENTÃO sistema DEVE retornar JSON com: nome_cidade, temperatura, temperatura_minima, temperatura_maxima, resumo_clima, coordenadas (lat/lon), timestamp, api_fonte
2. QUANDO usuário chama endpoint com nome de cidade válido ENTÃO sistema DEVE resolver coordenadas dinamicamente (sem valores hardcoded no código)
3. QUANDO usuário chama com cidade inexistente ENTÃO sistema DEVE retornar 404 com erro JSON:

```json
{
  "status": 404,
  "error_code": "CITY_NOT_FOUND",
  "message": "Cidade não encontrada",
  "details": "..."
}
```
4. QUANDO API climática externa está indisponível ENTÃO sistema DEVE retornar 503 com erro JSON:

```json
{
  "status": 503,
  "error_code": "EXTERNAL_SERVICE_ERROR",
  "message": "Serviço externo indisponível",
  "details": "..."
}
```
5. QUANDO nome de cidade tem < 2 caracteres ENTÃO sistema DEVE retornar 400 com erro JSON:

```json
{
  "status": 400,
  "error_code": "INVALID_INPUT",
  "message": "Entrada inválida",
  "details": "Nome da cidade deve ter >= 2 caracteres"
}
```

**Teste Independente:** Chamar `GET /api/v1/clima/fortaleza`, verificar resposta JSON com todos campos requeridos, validar temperatura em range válido (por ex., -50 a +60 para Terra), verificar timestamp é recente.

---

### P1: Usuários podem listar cidades por estado (UF) ⭐ MVP

**História de Usuário:** Como pesquisador, quero listar todas cidades em um estado dado (UF) para que eu possa descobrir localizações disponíveis para consultas de clima.

**Por que P1:** Acompanha consulta de clima; habilita descoberta de usuário; escopo MVP.

**Critérios de Aceitação:**

1. QUANDO usuário chama `GET /api/v1/cidades/SP` ENTÃO sistema DEVE retornar array JSON com: nome_cidade, codigo_estado e contagem de cidades totais
2. QUANDO chamado com código UF válido de 2 letras ENTÃO sistema DEVE retornar ≥10 cidades (para maioria dos UFs) originadas de IBGE Localidades
3. QUANDO chamado com UF inválido (não 2 letras ou código desconhecido) ENTÃO sistema DEVE retornar 404 com erro JSON:

```json
{
  "status": 404,
  "error_code": "STATE_NOT_FOUND",
  "message": "Estado não encontrado",
  "details": "..."
}
```
4. QUANDO chamado com UF minúscula (`get /api/v1/cidades/sp`) ENTÃO sistema DEVE normalizar para maiúscula e retornar resposta válida
5. QUANDO API IBGE está indisponível ENTÃO sistema DEVE retornar 503 com fallback para Brasil API se disponível

**Teste Independente:** Chamar `GET /api/v1/cidades/BA`, verificar array retornado, contagem > 1, primeira entrada tem campos requeridos, chamar com minúscula `ba` verificar normalização, testar com código inválido `XX` verificar 404.

---

### P1: Usuários podem consultar histórico de clima de uma cidade ⭐ MVP

**História de Usuário:** Como pesquisador, quero ver todas consultas passadas de clima para uma cidade para que eu possa rastrear padrões de consulta e analisar tendências históricas.

**Por que P1:** Persistência é valor central; habilita história de série temporal; escopo MVP.

**Critérios de Aceitação:**

1. QUANDO usuário chama `GET /api/v1/historico/rio-de-janeiro` ENTÃO sistema DEVE retornar array JSON de todas consultas passadas para essa cidade, ordenado por timestamp descendente
2. QUANDO não existe histórico para cidade ENTÃO sistema DEVE retornar array vazio `[]` com 200 (não 404)
3. QUANDO chamado ENTÃO cada registro histórico DEVE incluir: nome_cidade, codigo_estado, latitude, longitude, temperatura, temperatura_minima, temperatura_maxima, resumo_clima, consultado_em (ISO 8601), api_cidade_fonte, api_clima_fonte
4. QUANDO usuário consulta clima via `GET /api/v1/clima/{cidade}` ENTÃO essa consulta DEVE ser automaticamente salva em histórico dentro da mesma requisição
5. QUANDO nome de cidade é inválido (< 2 chars) ENTÃO sistema DEVE retornar 400 com erro validação

**Teste Independente:** (1) Chamar `GET /api/v1/clima/curitiba` duas vezes com tempos diferentes. (2) Chamar `GET /api/v1/historico/curitiba`. (3) Verificar 2 registros retornados, ordenados por mais recente primeiro, ambos com timestamps distintos. (4) Verificar cada registro tem todos campos requeridos.

---

### P1: Usuários podem consultar agregações de série temporal ⭐ MVP

**História de Usuário:** Como pesquisador, quero analisar tendências agregadas de clima (mín, máx, média) sobre múltiplas consultas para uma cidade para que eu possa identificar padrões climáticos.

**Por que P1:** Completa conjunto de funcionalidades central; demonstra valor de persistência; escopo MVP.

**Critérios de Aceitação:**

1. QUANDO usuário chama `GET /api/v1/serie/brasilia` ENTÃO sistema DEVE retornar JSON com: nome_cidade, quantidade_consultas, temperatura_media, temperatura_minima, temperatura_maxima, ultimo_consultado_em, intervalo_datas (início/fim)
2. QUANDO não existe histórico ENTÃO sistema DEVE retornar 200 com valores padrão: quantidade_consultas=0, _media/_minima/_maxima=null, ultimo_consultado_em=null
3. QUANDO existem múltiplas consultas ENTÃO agregações DEVEM ser calculadas de TODOS registros persistidos (não sampling)
4. QUANDO intervalo de datas span semanas ENTÃO sistema DEVE retornar mín/máx/média precisas sobre período completo (sem truncagem)
5. QUANDO chamado com nome de cidade inválido ENTÃO sistema DEVE retornar 400 com erro validação

**Teste Independente:** (1) Chamar `GET /api/v1/clima/manaus` 3 vezes (manualmente ou em loop, com variação de temperatura). (2) Chamar `GET /api/v1/serie/manaus`. (3) Verificar quantidade_consultas=3. (4) Verificar _minima ≤ _media ≤ _maxima. (5) Verificar intervalo_datas mostra span correto.

---

### P1: Verificação de saúde da API retorna JSON válido ⭐ MVP

**História de Usuário:** Como operador, quero verificar que API está rodando e todos serviços críticos estão saudáveis para que eu possa monitorar uptime e diagnosticar problemas rapidamente.

**Por que P1:** Fundacional; habilita monitoramento; requerido para verificação implantação.

**Critérios de Aceitação:**

1. QUANDO usuário chama `GET /api/v1/health` ENTÃO sistema DEVE retornar 200 JSON: `{ "status": "saudavel", "versao": "1.0.0", "timestamp": "...", "banco_dados": "conectado"|"desconectado" }`
2. QUANDO banco de dados está indisponível ENTÃO campo status DEVE ser "degradado" (não "saudavel"), campo banco_dados DEVE ser "desconectado"
3. QUANDO APIs externas não são alcançáveis ENTÃO status PODE ser "degradado" (opcional para v1; registre warning)
4. QUANDO chamado ENTÃO tempo de resposta DEVE ser < 100ms (sem chamadas externas, apenas verificações locais)
5. QUANDO porta 3000 está configurada ENTÃO endpoint health DEVE ser alcançável via `http://localhost:3000/api/v1/health`

**Teste Independente:** Chamar `GET /api/v1/health` via curl/Postman. Verificar status=saudavel, timestamp é ISO 8601, status banco_dados está presente. Verificar resposta < 100ms.

---

## Casos Extremos

- **QUANDO** nome de cidade tem caracteres especiais (ç, ã, é) **ENTÃO** sistema DEVE decodificar e corresponder corretamente em IBGE (por ex., "São Paulo")
- **QUANDO** nome de cidade tem múltiplas palavras (por ex., "Rio de Janeiro") **ENTÃO** sistema DEVE tratar como entidade única e corresponder corretamente
- **QUANDO** usuário fornece nome de cidade com whitespace extra ("  são paulo  ") **ENTÃO** sistema DEVE trim e processar
- **QUANDO** API externa responde com estrutura dados inesperada **ENTÃO** sistema DEVE retornar 503 (não 500) com mensagem descritiva
- **QUANDO** usuário fornece requisições rápidas duplicadas (< 1 sec apart) **ENTÃO** sistema DEVE registrar cada uma independentemente em histórico (sem deduplicação em v1)
- **QUANDO** histórico de consulta excede 1000 registros **ENTÃO** sistema DEVE ainda agregar corretamente (sem paginação em v1, mas deve estar preparado para v2)
- **QUANDO** cidade mudou coordenadas (raro) **ENTÃO** sistema DEVE usar dados IBGE atuais (não coords cache antigas)
- **QUANDO** temperatura é extrema (por ex., -100°C) **ENTÃO** sistema DEVE ainda retornar valor mas validar range é Terráqueo (-89 a +58)

---

## Rastreabilidade de Requisitos

| ID Requisito | História                              | Tipo             | Fase    | Status  |
| ------------ | ------------------------------------ | --------------- | ------- | ------- |
| CLI-01       | P1: Consultar clima por cidade      | API Central     | Specify | Pendente |
| CLI-02       | P1: Resolução geográfica dinâmica   | API Central     | Specify | Pendente |
| CLI-03       | P1: Tratamento erros (404, 503, 400)| API Central     | Specify | Pendente |
| CLI-04       | P1: Listar cidades por UF           | API Central     | Specify | Pendente |
| CLI-05       | P1: Consultar histórico             | API Central     | Specify | Pendente |
| CLI-06       | P1: Agregação série temporal        | API Central     | Specify | Pendente |
| CLI-07       | P1: Verificação saúde              | API Central     | Specify | Pendente |
| CLI-08       | P1: Persistência (auto-save)        | Persistência    | Specify | Pendente |
| CLI-09       | P1: Apenas respostas JSON           | Design API      | Specify | Pendente |
| CLI-10       | P1: CORS habilitado                 | Design API      | Specify | Pendente |
| CLI-11       | P1: Porta 3000                      | Configuração    | Specify | Pendente |

**Resumo:** 11 requisitos total | 0 mapeados para tasks (pendente fase Design) | 0 não mapeados

---

## Critérios de Sucesso

Como sabemos que a funcionalidade é bem-sucedida:

- [ ] Todos 5 endpoints (`health`, `clima`, `cidades`, `historico`, `serie`) respondem com JSON válido
- [ ] Todas histórias P1 têm ≥2 casos de teste independentes passando cada (cobrindo happy path + 1 caso erro)
- [ ] Respostas de erro são padronizadas (status, error_code, message, details) e correspondem a spec
- [ ] Coleção Postman inclui todos 5 endpoints com requisições de exemplo válidas + respostas
- [ ] README documenta todos endpoints com exemplos curl
- [ ] Sem coordenadas hardcoded em codebase (verificado via inspeção código)
- [ ] Agregações de série temporal verificadas corretas por spot-check manual (consultar 3 vezes, verificar mín/máx/média corresponde esperado)
- [ ] Endpoint health responde em < 100ms
- [ ] Funcionalidade pode ser demonstrada em < 5 minutos end-to-end (health → cities → clima → historico → serie)

---

## Notas para Fase Design

- **Camadas:** Confirmar camada Services trata lookup de cidade/clima; Repositories trata persistência
- **Mapeamento Erros:** Confirmar hierarquia exceção (InvalidCity, ExternalAPIUnavailable, ValidationError, etc.)
- **Considerações Async:** Chamadas httpx para IBGE/Open-Meteo devem ser async; confirmar em design
- **Estratégia Testes:** Mockar APIs externas em testes unitário/integração; considerar vcr.py ou biblioteca responses
- **Persistência:** Confirmar campos do modelo SQLAlchemy correspondem a coluna de tabela "Rastreabilidade Requisitos"
