# Manual de Padronização de Commits e Gitflow

Este manual define o padrão oficial de mensagens de commit e o fluxo de branches do projeto para manter o histórico legível, facilitar code review, organizar releases e reduzir ambiguidade entre desenvolvimento, homologação e produção.[1][2]

O time deve adotar dois pilares complementares: **Conventional Commits** para padronizar mensagens e **Gitflow** para organizar o ciclo de vida das branches do projeto.[1][2][3]

## Objetivos

A padronização existe para melhorar comunicação entre pessoas e ferramentas, permitir leitura rápida do histórico e tornar o processo de desenvolvimento mais previsível.[1][4]

Ela também apoia automações, versionamento, rastreabilidade por tarefa, preparação de release e correções emergenciais em produção.[1][2][5]

## Convenção de commits

O padrão adotado para mensagens é:

```text
<tipo>(<escopo-opcional>): <resumo>
```

Esse formato segue a especificação Conventional Commits, na qual o `tipo` é obrigatório, o `escopo` é opcional e o resumo deve descrever de forma objetiva a ação realizada.[1][6]

### Estrutura

- `tipo`: classifica a natureza da alteração, como `feat`, `fix`, `docs` ou `refactor`.[1][7]
- `escopo`: indica o módulo, pasta, contexto ou funcionalidade afetada, como `auth`, `api`, `health`, `tests` ou `config`.[6][7]
- `resumo`: frase curta, direta e escrita no imperativo, descrevendo o que o commit faz.[8][4]

### Exemplos válidos

```text
feat(api): add health endpoint
fix(auth): validate expired token
refactor(config): simplify settings loader
test(health): add health endpoint tests
docs(readme): update setup instructions
chore(deps): update fastapi version
```

Esses exemplos seguem a convenção porque começam com um tipo reconhecido, usam escopo quando útil e descrevem a mudança com verbo de ação.[1][9]

## Tipos permitidos

| Tipo | Quando usar | Exemplo |
|---|---|---|
| `feat` | Nova funcionalidade para o sistema | `feat(api): add weather search endpoint` [1][7] |
| `fix` | Correção de bug ou comportamento incorreto | `fix(cache): prevent stale response reuse` [1][7] |
| `docs` | Alteração apenas em documentação | `docs(readme): document local setup` [9][7] |
| `refactor` | Reorganização interna sem mudar comportamento funcional | `refactor(core): simplify config loading` [9][7] |
| `test` | Criação ou ajuste de testes sem alterar regra de negócio | `test(api): add forecast endpoint tests` [9][7] |
| `chore` | Mudanças operacionais, manutenção ou tooling | `chore(gitignore): ignore python cache files` [9][7] |
| `ci` | Mudanças em pipelines ou workflows | `ci(github): add pytest workflow` [9][7] |
| `build` | Mudanças de build, empacotamento ou dependências de build | `build(poetry): adjust script entrypoint` [7] |
| `perf` | Melhorias de performance | `perf(api): reduce response serialization overhead` [9][7] |
| `style` | Formatação sem alteração funcional | `style(lint): normalize import spacing` [9][6] |
| `revert` | Reversão de commit anterior | `revert(api): revert health response contract` [7] |

## Regras de escrita

### 1. Escrever no imperativo

A linha principal do commit deve ser escrita como comando, como `add`, `fix`, `remove`, `rename` ou `update`, porque a leitura implícita é “se aplicado, este commit vai...”.[8][10]

### 2. Resumo curto e específico

O resumo deve ser curto, objetivo e preferencialmente ficar em torno de 50 caracteres, deixando detalhes adicionais para o corpo quando necessário.[8][11]

### 3. Sem ponto final

A linha de assunto não deve terminar com ponto final, porque funciona como um título curto do commit.[8][4]

### 4. Um commit, uma intenção

Cada commit deve representar uma mudança coesa e única, facilitando revisão, rollback e rastreabilidade.[11]

## Padrão com ID de tarefa

Quando houver tarefa formal, o time pode incluir o identificador no escopo ou no resumo, desde que a mensagem continue legível.[1][7]

Exemplos:

```text
feat(T01): setup FastAPI app and health endpoint
fix(T02-auth): validate missing token
docs(T03): document branch strategy
```

## Gitflow adotado no projeto

O projeto passa a adotar o modelo **Gitflow**, que organiza o trabalho em branches com papéis claros para desenvolvimento contínuo, preparação de release e correções urgentes.[2][3]

Nesse modelo, `main` representa a linha de produção, `develop` representa a linha de integração de desenvolvimento, `feature/*` concentra novas funcionalidades, `release/*` prepara versões e `hotfix/*` trata correções urgentes saídas de produção.[2][5][12]

## Branches oficiais

| Branch | Finalidade | Origem | Destino principal |
|---|---|---|---|
| `main` | Produção, histórico estável e versões publicadas | — | Recebe `release/*` e `hotfix/*` [2][5] |
| `develop` | Integração contínua do próximo ciclo de desenvolvimento | `main` na inicialização do fluxo | Recebe `feature/*`, `release/*` e `hotfix/*` [2][12] |
| `feature/*` | Desenvolvimento de funcionalidades isoladas | `develop` | `develop` [2][13] |
| `release/*` | Estabilização de versão antes da produção | `develop` | `main` e `develop` [2][5] |
| `hotfix/*` | Correções urgentes em produção | `main` | `main` e `develop` [2][5][14] |

## Convenção de nomes de branches

O projeto deve seguir a seguinte convenção:

```text
main
develop
feature/Txx-nome-curto
release/x.y.z
hotfix/x.y.z-descricao-curta
```

Exemplos:

```text
feature/T01-setup-api-health
feature/T02-add-weather-search
release/0.1.0
hotfix/0.1.1-health-timeout
```

Essa convenção facilita rastreabilidade, leitura rápida e associação entre branch, tarefa e objetivo técnico.[2][12]

## Fluxo padrão de desenvolvimento

### 1. Partir de `develop`

Toda nova funcionalidade deve nascer a partir da branch `develop`, porque ela é a branch de integração das próximas entregas.[2][12]

```bash
git checkout develop
git pull origin develop
git checkout -b feature/T02-add-weather-search
```

### 2. Trabalhar em `feature/*`

A implementação deve acontecer na branch de feature, com commits pequenos, semânticos e alinhados ao padrão Conventional Commits.[1][2]

Exemplo de sequência saudável:

```text
feat(api): add weather search endpoint
test(api): add weather endpoint tests
refactor(core): extract weather service config
docs(readme): document weather endpoint usage
```

### 3. Integrar de volta em `develop`

Quando a feature estiver validada, ela deve ser mergeada em `develop`, preferencialmente com histórico claro e validações executadas antes do merge.[2][13]

Fluxo simplificado:

```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/T02-add-weather-search
git push origin develop
```

### 4. Criar `release/*`

Quando `develop` estiver estável para uma entrega, cria-se uma branch de release para testes finais, pequenos ajustes e preparação da versão.[2][5]

```bash
git checkout develop
git pull origin develop
git checkout -b release/0.1.0
```

Na `release/*`, devem entrar apenas ajustes de estabilização, documentação final, correções pequenas e tarefas necessárias para empacotar a versão.[2][5]

### 5. Publicar release

Quando a release estiver aprovada, ela deve ser mergeada em `main` e também de volta em `develop`, para garantir que correções feitas na estabilização não se percam no fluxo futuro.[2][5][12]

```bash
git checkout main
git pull origin main
git merge --no-ff release/0.1.0
git push origin main

git checkout develop
git pull origin develop
git merge --no-ff release/0.1.0
git push origin develop
```

Depois disso, a branch `release/0.1.0` pode ser removida.[2][12]

### 6. Corrigir produção com `hotfix/*`

Se houver erro crítico em produção, a correção deve nascer de `main` em uma branch `hotfix/*`, nunca diretamente de `develop`.[2][5][14]

```bash
git checkout main
git pull origin main
git checkout -b hotfix/0.1.1-health-timeout
```

Depois da correção, o hotfix deve ser mergeado em `main` e também em `develop`, para que a correção de produção continue presente no fluxo de desenvolvimento.[2][5][14]

## Regras operacionais do time

- Nunca desenvolver direto em `main`.[2][3]
- Nunca desenvolver funcionalidade direto em `develop`; usar sempre `feature/*`.[2][13]
- Toda `feature/*` nasce de `develop` e volta para `develop`.[2][12]
- Toda `release/*` nasce de `develop` e volta para `main` e `develop`.[2][5]
- Todo `hotfix/*` nasce de `main` e volta para `main` e `develop`.[2][5][14]
- Commits devem seguir Conventional Commits em qualquer tipo de branch.[1][7]

## Exemplo prático para o projeto

### Implementação de nova tarefa

```bash
git checkout develop
git pull origin develop
git checkout -b feature/T03-add-climate-search
```

Commits possíveis nessa branch:

```text
feat(api): add climate search endpoint
test(api): add climate search integration tests
refactor(core): extract climate provider factory
docs(api): document climate search contract
```

Integração:

```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/T03-add-climate-search
git push origin develop
```

### Correção urgente em produção

```bash
git checkout main
git pull origin main
git checkout -b hotfix/0.1.1-invalid-health-status
```

Commit possível:

```text
fix(health): return correct status on provider timeout
```

Depois:

```bash
git checkout main
git merge --no-ff hotfix/0.1.1-invalid-health-status
git push origin main

git checkout develop
git merge --no-ff hotfix/0.1.1-invalid-health-status
git push origin develop
```

## O que evitar

Evitar estes padrões porque reduzem clareza e utilidade do histórico:

- `update`
- `ajustes`
- `correções`
- `wip`
- `temp`
- `teste`
- `mudanças diversas`
- `commit final`
- `subindo projeto`

Também deve ser evitado:

- commit grande com várias intenções misturadas;[11]
- abrir feature a partir de `main`;[2][13]
- corrigir produção em `develop`;[2][5]
- esquecer de propagar `release` e `hotfix` de volta para `develop`.[2][5]

## Checklist antes de commitar e integrar

1. Confirmar que a alteração tem uma intenção única e clara.[11]
2. Escolher o tipo correto do commit.[1][7]
3. Definir escopo quando ajudar a localizar a mudança.[6][7]
4. Escrever resumo curto no imperativo e sem ponto final.[8][4]
5. Garantir que a branch correta está sendo usada no Gitflow.[2][3]
6. Rodar validações mínimas antes de merge, como testes, lint e revisão do diff.[2][15]
7. Fazer merge para o destino certo: `feature -> develop`, `release -> main + develop`, `hotfix -> main + develop`.[2][5]

## Modelo rápido para uso diário

### Commit

```text
<tipo>(<escopo>): <ação objetiva>
```

### Branch

```text
feature/Txx-descricao-curta
release/x.y.z
hotfix/x.y.z-descricao-curta
```

## Regra final do time

Se o histórico não permitir entender rapidamente **o que mudou**, **onde mudou**, **por que mudou** e **em qual etapa do fluxo Gitflow essa mudança entrou**, então o commit ou a branch devem ser ajustados antes da integração.[4][2]

O histórico Git e a estratégia de branches fazem parte da documentação técnica viva do projeto, então commits e branches devem ser tratados como artefatos de engenharia, não como detalhes operacionais sem importância.[1][2]