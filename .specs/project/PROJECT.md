# API de Pesquisa em Clima

**Visão:** Construir uma API REST em Python que agregue dados geográficos e meteorológicos com foco em persistência de histórico e suporte a análises temporais.

**Para:** Pesquisadores e profissionais de clima/meteorologia; demonstração técnica para portfólio profissional.

**Resolve:** Consultas de clima por nome de cidade (dinâmicas, sem coordenadas fixas), histórico de consultas e análises temporais.

## Objetivos

- [ ] **MVP:** Entregar endpoints funcionais para buscar clima por cidade, listar cidades por UF e consultar histórico
  - Sucesso: 5 endpoints ativos, cobertura de testes P1 > 80%, zero erros padrão
- [ ] **Integridade de Dados:** Persistir todas as consultas com rastreabilidade completa (fonte da API, timestamp, coordenadas)
  - Sucesso: Histórico recuperável e auditável, pronto para futura migração PostgreSQL
- [ ] **Portfólio:** Demonstrar arquitetura em camadas, padrões pythônicos e boas práticas de API
  - Sucesso: README claro, coleção Postman funcional, INTEGRANTES.md documentado

## Stack Tecnológico

**Núcleo:**

- Linguagem: Python 3.10+
- Framework: FastAPI
- Banco de Dados: SQLite (v1), PostgreSQL (migração futura preparada)
- ORM: SQLAlchemy
- Cliente HTTP: httpx
- Testes: pytest

**Dependências-chave:**
- FastAPI → Framework de API RESTful
- SQLAlchemy → ORM + camada de dados
- httpx → Cliente HTTP assíncrono para APIs externas
- pytest → Framework de testes
- python-dotenv → Configuração de ambiente

## Escopo

**v1 inclui:**

- `GET /api/v1/health` → Verificação de saúde
- `GET /api/v1/clima/{nome_cidade}` → Consultar clima por nome de cidade (resolução geográfica dinâmica)
- `GET /api/v1/cidades/{sigla_uf}` → Listar cidades por código de estado (UF)
- `GET /api/v1/historico/{nome_cidade}` → Consultar histórico para uma cidade
- `GET /api/v1/serie/{nome_cidade}` → Agregação de série temporal (médias, mín/máx)
- Tratamento global de erros (400, 404, 503 com JSON padronizado)
- CORS habilitado na porta 3000
- Camada de persistência SQLite com tabela `query_history`
- Cobertura de testes para health, clima e cidades

**Explicitamente fora do escopo:**

- Autenticação / autorização (v1)
- Contas de usuário ou chaves de API
- Notificações por webhook
- Streaming de dados em tempo real
- Componentes frontend / UI
- Migração PostgreSQL (preparada, não implementada)
- Preenchimento retroativo de clima histórico
- Cálculos de métricas de clima customizadas além dos dados da API fonte

## Restrições

- **Timeline:** Alvo de MVP v1 (sem data-limite específica no PRD)
- **Técnicas:** Usar apenas APIs públicas (IBGE, Brasil API, Open-Meteo); sem coordenadas fixas no código; todas respostas em JSON
- **Arquitetura:** Em camadas (routes → services → repositories → models); sem handlers monolíticos
