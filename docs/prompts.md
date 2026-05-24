Segue uma versão **nova** para o `docs/prompts.md`, já alinhada com:

- tlc-spec-driven (`.specs/project/*`, `.specs/features/api-pesquisa-clima/*`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_f45b5e69-c0ec-4f1f-86d7-6e132dbd647b/06f9561e-49ac-4759-a8c0-c6b75f590665/Spec-Driven-Development.txt)
- tasks T01–T17. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_f45b5e69-c0ec-4f1f-86d7-6e132dbd647b/277e06e5-632d-4358-9e56-654b80d566e8/fluxo-COMPLETO-de-desenvolvimento-avancado-com-IA.txt)
- uso do Context7 para docs de FastAPI/SQLAlchemy/httpx/APIs externas. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_f45b5e69-c0ec-4f1f-86d7-6e132dbd647b/277e06e5-632d-4358-9e56-654b80d566e8/fluxo-COMPLETO-de-desenvolvimento-avancado-com-IA.txt)
- novo contrato de erro (`status`, `error_code`, `message`, `details`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_f45b5e69-c0ec-4f1f-86d7-6e132dbd647b/063badb1-cc23-48fa-8c44-64100871a89c/Spec-Driven-chegou-no-limite1.txt)

Pode substituir o conteúdo do arquivo atual por este.

***

```markdown
# Prompts para Desenvolvimento com IA — API de Pesquisa em Clima

Este projeto segue **Spec-Driven Development** com a skill `tlc-spec-driven`:

> Specify → Design → Tasks → Execute

Os artefatos principais de especificação estão em:

- `.specs/project/PROJECT.md`, `ROADMAP.md`, `STATE.md`
- `.specs/features/api-pesquisa-clima/spec.md`
- `.specs/features/api-pesquisa-clima/design.md`
- `.specs/features/api-pesquisa-clima/tasks.md`

Abaixo estão prompts **genéricos** para usar com Copilot/Claude/Cursor/Windsurf em VS Code, sempre respeitando esse fluxo.


## 0. Regras gerais para qualquer prompt

Sempre inclua (explícita ou implicitamente):

- Idioma: respostas **em português do Brasil (pt-BR)**.
- Contexto local prioritário:
  - `.specs/project/PROJECT.md`, `ROADMAP.md`, `STATE.md`
  - `.specs/features/api-pesquisa-clima/spec.md`, `design.md`, `tasks.md`
  - `docs/api-pesquisa-clima-prd.md`
  - `docs/architecture-rules.md`
  - `docs/routes-guidelines.md`
  - `docs/error-handling.md`
  - `docs/persistence-guidelines.md`
  - `docs/testing-guidelines.md`
  - `docs/checklists.md`
- Context7 MCP:
  - Para qualquer dúvida sobre **FastAPI, SQLAlchemy, httpx, pytest, IBGE, Brasil API, Open‑Meteo**, usar Context7 para consultar a documentação oficial (não inventar APIs nem parâmetros).

Formato padrão de erro da API:

```json
{
  "status": <http_status:int>,
  "error_code": "<CÓDIGO_INTERNO:string>",
  "message": "<mensagem em pt-BR>",
  "details": null | { ... }
}
```


---

## 1. Revisar consistência entre PRD, SPEC, DESIGN e docs

Use quando atualizar PRD ou alguma regra em `docs/` e quiser que a IA aponte incoerências antes de mexer em código.

```text
Quero que você atue como revisor técnico da documentação deste projeto,
NÃO gerando novos arquivos ainda, apenas apontando ajustes necessários.

Regra fixa:
- Sempre usar português do Brasil (pt-BR) nas explicações.

Contexto principal:
- Projeto: .specs/project/PROJECT.md
- Roadmap: .specs/project/ROADMAP.md
- Memória do projeto: .specs/project/STATE.md
- Especificação da feature: .specs/features/api-pesquisa-clima/spec.md
- Design técnico: .specs/features/api-pesquisa-clima/design.md
- PRD detalhado: docs/api-pesquisa-clima-prd.md
- Regras técnicas:
  - docs/architecture-rules.md
  - docs/routes-guidelines.md
  - docs/error-handling.md
  - docs/persistence-guidelines.md
  - docs/testing-guidelines.md
  - docs/checklists.md

Uso de documentação externa:
- Se precisar de detalhes de frameworks/APIs (FastAPI, SQLAlchemy, httpx, pytest,
  IBGE Localidades, Brasil API, Open‑Meteo), use o MCP Context7.
- Não invente APIs ou comportamentos.

Tarefas:
1) Ler TODOS esses arquivos e verificar:
   - Consistência entre PRD ⇄ SPEC ⇄ DESIGN ⇄ PROJECT/ROADMAP.
   - Se todos os endpoints planejados estão refletidos na SPEC e no design.
   - Se regras importantes aparecem claramente:
     - Validações de `nome_cidade` e `sigla_uf`.
     - Erros 400, 404, 503 e 500 com o payload de erro padronizado.
     - Uso de APIs públicas sem coordenadas fixas.
     - Uso da tabela query_history para histórico e séries.

2) Me devolver um relatório em tópicos, em pt-BR, contendo:
   - Pontos que estão OK e claros.
   - Pontos faltando ou incoerentes, com indicação do arquivo e seção.
   - Sugestões concretas de ajustes (arquivo + trecho + sugestão).

3) Não reescreva ainda os arquivos.
   - Apenas liste o que precisa ser ajustado, para eu decidir o que aplicar depois.
```


---

## 2. Executar uma task específica do `tasks.md` (fase Execute)

Prompt base para implementar **uma** task de `.specs/features/api-pesquisa-clima/tasks.md` por vez  
(ex.: T01 – setup base da API e health, T02 – database, etc.).

```text
Use a skill tlc-spec-driven.

Regra fixa:
- Código e comentários em português quando fizer sentido,
  mantendo nomes de tipos, endpoints e identificadores em inglês.
- Sempre rodar testes ao final da tarefa.

Contexto:
- Projeto: .specs/project/PROJECT.md, ROADMAP.md, STATE.md
- Feature: .specs/features/api-pesquisa-clima/spec.md
- Design: .specs/features/api-pesquisa-clima/design.md
- Tasks: .specs/features/api-pesquisa-clima/tasks.md
- Guidelines técnicas:
  - docs/architecture-rules.md
  - docs/routes-guidelines.md
  - docs/error-handling.md
  - docs/persistence-guidelines.md
  - docs/testing-guidelines.md
  - docs/checklists.md

Uso de documentação externa:
- Para qualquer dúvida sobre FastAPI, SQLAlchemy, httpx, pytest,
  IBGE Localidades, Brasil API ou Open‑Meteo, use o MCP Context7
  para consultar a documentação oficial. Não invente APIs nem parâmetros.

Tarefa a executar AGORA:
- Implementar APENAS a seguinte task (copie aqui o bloco exato do tasks.md):

[COLE AQUI O BLOCO DA TASK Txx, incluindo What/Where/Done when/Tests]

Regras de execução:
1) Antes de escrever código, liste de forma sucinta os passos que você vai seguir
   para cumprir esta task, com base em "What", "Where", "Depends on", "Done when" e "Tests".

2) Depois implemente os arquivos necessários em src/ e tests/,
   seguindo os padrões definidos em docs/*-guidelines.md
   (rotas finas, lógica em services, erros padronizados, testes bem isolados).

3) Ao final:
   - Execute os testes indicados em "Tests" (ex.: `pytest tests/test_health.py -q`).
   - Confirme se todos os critérios de "Done when" foram atendidos.
   - Liste claramente os arquivos criados/alterados.
```

Sugestão de ordem para uso prático:

- T01 → setup base + `/health`.
- T02 → `config` + `database`.
- T03/T04/T05 → schemas + modelo + repositório.
- T06–T11 → clients externos, services, rotas.
- T12–T15 → erros, testes unitários e de integração.
- T16–T17 → docs e limpeza final.


---

## 3. Quick fix / tarefa pequena fora do fluxo principal

Use quando quiser fazer uma mudança bem localizada (≤ 3 arquivos) sem passar pelo ciclo completo `Specify → Design → Tasks`.  
Exemplos: ajustar uma mensagem de erro, renomear um campo de schema, corrigir um teste.

```text
Quero fazer uma correção pequena e localizada neste projeto, em quick mode.

Regra fixa:
- Sempre responder em português do Brasil (pt-BR).
- Não alterar a estrutura de `.specs/` nem o design geral da feature.

Contexto relevante:
- Projeto e feature:
  - .specs/project/PROJECT.md, ROADMAP.md, STATE.md
  - .specs/features/api-pesquisa-clima/spec.md, design.md, tasks.md
- Regras técnicas:
  - docs/architecture-rules.md
  - docs/routes-guidelines.md
  - docs/error-handling.md
  - docs/persistence-guidelines.md
  - docs/testing-guidelines.md

Mudança desejada (explique aqui em 1–2 frases):
- Exemplo: “Atualizar a mensagem de erro do endpoint de clima quando cidade não for encontrada.”

Tarefas:
1) Identificar quais arquivos precisam ser alterados (máx. 3 arquivos).
2) Propor o diff mínimo necessário para implementar essa correção, mantendo compatibilidade com:
   - SPEC e DESIGN
   - formato de erro (status, error_code, message, details)
   - testes existentes
3) Mostrar o diff em blocos (antes → depois) para eu revisar.

Não criar novas features nem mexer em tasks maiores; tratar apenas essa correção pontual.
```
```