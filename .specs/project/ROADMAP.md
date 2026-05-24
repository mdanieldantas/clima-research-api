# Roadmap — API de Pesquisa em Clima

## v1.0.0 — MVP (Marco: API Central + Persistência + Histórico)

### Marco 1: Fundação e Configuração
**Objetivo:** Estabelecer estrutura do projeto, dependências e configuração base
- [ ] Estrutura de repositório definida (src/, tests/, docs/)
- [ ] Ambiente Python (requirements.txt / pyproject.toml)
- [ ] Aplicação FastAPI com CORS e porta 3000
- [ ] Gerenciamento básico de configuração (core/config.py)
- [ ] README.md e INTEGRANTES.md
- **Gate de Conclusão:** `GET /api/v1/health` responde com JSON

### Marco 2: Tratamento de Erros e Fundação da API
**Objetivo:** Padronizar respostas de erro, criar manipulação base de exceções
- [ ] Manipuladores globais de exceção (400, 404, 503 → payloads JSON)
- [ ] Classes de exceção customizadas (InvalidCityException, ExternalAPIException, etc.)
- [ ] Schema de erro (code, message, details)
- [ ] Testes para cenários de erro
- **Gate de Conclusão:** 3 cenários de erro testados (entrada inválida, não encontrado, serviço externo indisponível)

### Marco 3: Integração Geográfica (Cidades e Estados)
**Objetivo:** Buscar cidades por estado, resolver coordenadas de cidade dinamicamente
- [ ] Serviço de cidades com integração IBGE/Brasil API
- [ ] Endpoint `GET /api/v1/cidades/{sigla_uf}`
- [ ] Validação de UF (2 letras)
- [ ] Normalização de resposta
- [ ] Testes para happy path + casos de erro
- **Gate de Conclusão:** Pode listar cidades para qualquer UF válido e tratar estados inválidos graciosamente

### Marco 4: Integração Climática
**Objetivo:** Buscar dados climáticos via Open-Meteo, resolver dinâmicamente lat/lon
- [ ] Serviço de clima com integração Open-Meteo
- [ ] Resolução dinâmica de cidade → coordenadas (sem lat/lon hardcoded no código)
- [ ] Endpoint `GET /api/v1/clima/{nome_cidade}`
- [ ] Normalização de resposta (temperatura, resumo, metadados)
- [ ] Testes para cidades válidas + casos de erro (não encontrado, API indisponível)
- **Gate de Conclusão:** Pode consultar clima para qualquer cidade brasileira por nome

### Marco 5: Persistência e Histórico
**Objetivo:** Armazenar histórico de consultas, habilitar análise de série temporal
- [ ] Modelos SQLAlchemy (QueryHistory)
- [ ] Configuração banco SQLite (core/database.py)
- [ ] Configuração de migração (se usar Alembic; opcional para v1)
- [ ] Repositório de histórico (camada de persistência)
- [ ] Salvar metadados de consulta de clima após cada requisição `clima`
- [ ] Endpoint `GET /api/v1/historico/{nome_cidade}`
- [ ] Endpoint `GET /api/v1/serie/{nome_cidade}` (agregações: média temp, mín/máx)
- [ ] Testes para persistência e recuperação
- **Gate de Conclusão:** Histórico persiste entre requisições, agregações de série funcionam corretamente

### Marco 6: Testes e Documentação
**Objetivo:** Atingir cobertura de testes MVP, documentar API
- [ ] Fixtures pytest para mockar APIs externas
- [ ] Testes unitários (services, repositories)
- [ ] Testes de integração (endpoints)
- [ ] Cobertura de testes > 80% (histórias P1)
- [ ] Coleção Postman (todos 5 endpoints, requisições de exemplo)
- [ ] Documentação de API inline (docstrings)
- **Gate de Conclusão:** Todas histórias P1 com testes passando + coleção Postman válida

---

## v1.1.0 — Refinamentos (Pós-MVP)
- [ ] Deduplicação de consultas (evitar logging de consultas idênticas consecutivas)
- [ ] Rate limiting (se necessário para APIs públicas)
- [ ] Paginação para histórico grande / listas de cidades
- [ ] Cache de resposta para consultas geo/clima (opcional)
- [ ] Logging aprimorado / logs estruturados
- [ ] Configuração de pipeline CI/CD (GitHub Actions / GitLab CI)

---

## v2.0.0 — Scaling e Funcionalidades Avançadas
- [ ] Suporte de migração PostgreSQL (versionamento schema com Alembic)
- [ ] Autenticação e chaves de API
- [ ] Contas de usuário para quotas de consulta
- [ ] Notificações por webhook para alertas de clima
- [ ] Análise avançada de série temporal (tendências, anomalias)
- [ ] Preenchimento retroativo de dados climáticos históricos
- [ ] Endpoint GraphQL (opcional)
- [ ] Containerizar aplicação (Docker)

---

## Dependências e Riscos

### Dependências Conhecidas
- Marco 2 deve completar antes Marco 4 (tratamento de erros → endpoint clima)
- Marco 3 deve completar antes Marco 5 (resolução de cidades → persistência histórico)

### Dependências de API Externa
- **IBGE Localidades** (cidades) — pública, confiável, sem autenticação requerida
- **Open-Meteo** (clima) — pública, confiável, sem autenticação requerida
- **Brasil API** (backup para cidades) — pública, confiável

### Bandeiras de Risco
- 🔴 **Disponibilidade de API externa** — Se IBGE ou Open-Meteo caem, endpoints relacionados falham
  - *Mitigação:* Mockar APIs externas em testes; implementar fallback para Brasil API em cidades
- 🟡 **Precisão de coordenadas** — Qualidade de resolução geográfica dinâmica depende dados IBGE
  - *Mitigação:* Validar ranges lat/lon antes de passar para API climática
- 🟡 **Limitações SQLite** — Não adequado para escala produção
  - *Mitigação:* Desenhar repositórios para suportar PostgreSQL em v2 com mudanças schema mínimas
