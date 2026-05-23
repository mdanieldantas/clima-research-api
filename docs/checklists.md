# checklists – desenvolvimento assistido por ia

este arquivo traz checklists rápidos para usar ia com segurança neste projeto.

---

## checklist geral por tarefa (rpi – research, plan, implement)

### 1. contexto e preparação

- [ ] abri um chat/aba nova só para **esta tarefa** (evitar contexto poluído).
- [ ] tenho claro **qual endpoint/feature** vou mexer (ex.: `get /api/v1/clima/{nome_cidade}`).
- [ ] verifiquei se os docs relacionados estão atualizados:
  - [ ] `architecture-rules.md`
  - [ ] `docs/routes-guidelines.md`
  - [ ] `docs/error-handling.md`
  - [ ] `docs/persistence-guidelines.md`
  - [ ] `docs/testing-guidelines.md`

### 2. research (pesquisa)

- [ ] pedi para a ia **ler os docs relevantes** e resumir o que precisa ser feito nesta tarefa.
- [ ] confirmei que:
  - [ ] os requisitos da tarefa estão claros (rotas, payloads, erros, persistência, testes).
  - [ ] não falta nenhuma decisão importante (ex.: formato de resposta, códigos de erro).

### 3. plan (plano)

- [ ] pedi para a ia gerar um **plano de passos** antes de escrever código, incluindo:
  - [ ] lista de arquivos que serão criados/alterados.
  - [ ] resumo das mudanças em cada arquivo.
  - [ ] comandos de validação (ex.: `pytest`, `uvicorn`, etc.).
- [ ] revisei o plano como “tech lead”:
  - [ ] removi coisas desnecessárias.
  - [ ] ajustei nomes de arquivos e funções para seguir os guidelines.
  - [ ] dividi em sub-tarefas se o plano ficou grande demais.

### 4. implement (implementação)

- [ ] pedi para a ia implementar **apenas a tarefa atual**, seguindo o plano:
  - [ ] sem misturar features diferentes na mesma rodada.
  - [ ] pedindo sempre “mostre o conteúdo completo dos arquivos criados/alterados”.
- [ ] revisei manualmente o diff de código:
  - [ ] verifiquei se tudo respeita os docs de arquitetura, rotas, erros, persistência e testes.
  - [ ] garanti que não surgiram “atalhos” (ex.: coordenadas hardcoded, respostas sem schema, etc.).

### 5. validações (completion gates)

- [ ] rodei `pytest` na raiz do projeto.
- [ ] (opcional) rodei ferramentas de lint/format (ex.: `ruff`, `black`, se estiverem configuradas).
- [ ] levantei a api (`uvicorn src.main:app --reload` ou comando equivalente).
- [ ] testei manualmente os endpoints afetados (ex.: via postman/insomnia):
  - [ ] cenários de sucesso (200).
  - [ ] cenários de erro principais (400, 404, 503) com payloads de erro padronizados.
- [ ] confirmei que:
  - [ ] não quebrei endpoints existentes.
  - [ ] os testes de regressão continuam passando.

### 6. pós-tarefa

- [ ] atualizei algum `.md` de guidelines se aprendi algo novo que vale virar padrão.
- [ ] fiz commit com uma mensagem clara (ex.: `feat: add clima endpoint with history`).
- [ ] fechei o chat/aba da ia para não acumular contexto desnecessário na próxima tarefa.

---

## checklist rápida para criar um novo endpoint

- [ ] definir claramente o objetivo do endpoint (rota, payload, response, erros).
- [ ] atualizar/verificar `docs/routes-guidelines.md` se necessário.
- [ ] pedir para a ia:
  - [ ] criar/ajustar rota em `src/api/routes/...`.
  - [ ] criar/ajustar schemas em `src/schemas/...`.
  - [ ] criar/ajustar serviços em `src/services/...`.
  - [ ] criar/ajustar testes em `tests/test_*.py`.
- [ ] validar com `pytest` + testes manuais no endpoint.