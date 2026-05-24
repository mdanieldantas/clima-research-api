# Estado do Projeto e Memória

**Última Atualização:** 2026-05-23
**Fase Atual:** Specify → Pronto para Design
**Sessão:** Inicialização TLC Spec-Driven

---

## Decisões Tomadas

### Decisão 1: Escopo MVP de Funcionalidade Única
- **Decisão:** v1 entregará uma funcionalidade completa (API de Pesquisa em Clima) com todos 5 endpoints
- **Racional:** Alinhado com PRD; fornece slice vertical completa para demo/portfólio
- **Impacto:** Entrega inicial mais simples; adia autenticação, WebSockets, funcionalidades multi-usuário para v2
- **Status:** ✅ Confirmado

### Decisão 2: Estratégia de API Externa
- **Decisão:** Usar IBGE Localidades (primária) + Brasil API (fallback) para cidades; Open-Meteo para clima
- **Racional:** APIs públicas, sem autenticação requerida, confiáveis, alinhadas com recomendações PRD
- **Risco:** Se primária e fallback caem, endpoint cidades falha → mitigação na fase Design
- **Status:** ✅ Confirmado

### Decisão 3: Estratégia de Persistência (v1)
- **Decisão:** SQLite para v1; desenhar schema para suportar migração PostgreSQL em v2 (sem Alembic/migrações em v1)
- **Racional:** Simples para MVP, suficiente para demo portfólio, reduz escopo
- **Impacto:** Versionamento manual de schema; caminho de migração preparado na arquitetura
- **Status:** ✅ Confirmado

### Decisão 4: Padronização de Erros
- **Decisão:** Todos os erros retornam JSON (nunca HTML); schema padronizado deve ser:

```json
{
  "status": <http_status:int>,
  "error_code": "<CÓDIGO_INTERNO:string>",
  "message": "<mensagem em pt-BR>",
  "details": null | { ... }
}
```

- **Racional:** Separar o `status` HTTP do `error_code` interno facilita logs, testes e mapeamento de exceções sem confundir o transport-layer.
- **Impacto:** Manipuladores globais de exceção devem construir o `status` e o `error_code` de forma explícita; atualizar exemplos e testes.
- **Status:** ✅ Confirmado

---

## Bloqueadores

Nenhum identificado na fase Specify. Pronto para proceder para Design.

---

## Ideias Adiadas (Pós-MVP)

- Deduplicação de consultas (evitar logging de consultas idênticas consecutivas)
- Rate limiting para tiers de API pública
- Paginação para listas grandes de cidades / registros histórico
- Cache de resposta (Redis) para consultas geo/clima
- Logging estruturado / observabilidade
- Integração de pipeline CI/CD
- Autenticação por nível de consulta e quotas de usuário (v2)
- Analytics avançada (detecção de tendências, anomalias)
- Preenchimento retroativo de clima histórico
- Endpoint GraphQL

---

## Débito Técnico / Preocupações

- 🟡 **Escalabilidade SQLite:** Se volume de consulta cresce > 10k registros, considerar migração PostgreSQL mais cedo
  - *Mitigação:* Desenhar repositórios para suportar ambos; documentar procedimento de troca
- 🟡 **Confiabilidade de API externa:** Indisponibilidade de IBGE/Open-Meteo bloqueia funcionalidade
  - *Mitigação:* Implementar padrão circuit breaker ou cache fallback (v1.1)
- 🟡 **Precisão de coordenadas:** IBGE pode ter dados desatualizados para cidades novas
  - *Mitigação:* Usar IBGE sempre como fonte de verdade; documentar limites de precisão em README

---

## Lições Aprendidas

- PRD foi bem estruturado; perguntas mínimas de esclarecimento necessárias
- Histórias de usuário mapeiam limpaamente para endpoints (proporção 1:1)
- Tabela de escopo (fora de escopo) previne scope creep efetivamente

---

## Próximos Passos

1. **Fase Design:** Arquitetura + componentes + hierarquia de exceções
2. **Fase Tasks:** (se necessário baseado na complexidade Design)
3. **Fase Execute:** Implementar services, repositories, routes; escrever testes
4. **Fase Validate:** Demo funcionalidade end-to-end; verificar todos critérios aceitação P1

---

## Rastreador de Progresso da Sessão

| Atividade                | Completo | Data       |
| ----------------------- | --------- | ---------- |
| PROJECT.md criado       | ✅         | 2026-05-23 |
| ROADMAP.md criado       | ✅         | 2026-05-23 |
| spec.md criado          | ✅         | 2026-05-23 |
| Fase Specify            | ✅         | 2026-05-23 |
| Fase Design             | ⏳ Pronto | —          |
