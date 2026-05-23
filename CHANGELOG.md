# changelog – api de pesquisa em clima

todas as mudanças relevantes neste projeto serão documentadas aqui.

este arquivo segue este padrão:

- cada seção de versão tem o formato: `## [vX.Y.Z] – descrição curta`
- dentro de cada versão, usar subtítulos:
  - `### adicionado`
  - `### alterado`
  - `### removido` (se necessário)
- a seção `[unreleased]` é usada para mudanças ainda não “fechadas” em uma versão.

quando pedir para a ia atualizar esse arquivo, use instruções como:
- “adicione um item em `## [unreleased]` > `### adicionado` descrevendo a nova funcionalidade x”.
- “mova os itens de `## [unreleased]` para uma nova seção `## [v0.2.0] – ...`”.

---

## [unreleased]

### adicionado
- (aqui vão entrar mudanças que ainda não fechei como uma versão. peça para a ia substituir este texto por itens reais quando necessário.)

### alterado
- (use esta seção para mudanças em comportamento existente, refactors, etc.)

### removido
- (use esta seção se algo importante foi removido.)

---

## [v0.1.0] – base da api

### adicionado
- arquivo `architecture-rules.md` com visão geral da arquitetura e regras para ia.
- arquivos em `docs/`:
  - `routes-guidelines.md`
  - `error-handling.md`
  - `persistence-guidelines.md`
  - `testing-guidelines.md`
  - `checklists.md`
- estrutura inicial para desenvolvimento assistido por ia (guidelines + checklists).

### alterado
- (vazio – nada foi alterado nesta primeira versão.)

### removido
- (vazio – nada foi removido nesta primeira versão.)