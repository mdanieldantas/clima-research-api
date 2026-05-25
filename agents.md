# Mapa Principal da IA

Este arquivo é o mapa principal da IA neste repositório.
Use-o para localizar contexto, entender precedência e escolher o documento certo para cada tarefa.

## Ponto de partida

1. [.github/copilot-instructions.md](.github/copilot-instructions.md)
2. [.specs/project/PROJECT.md](.specs/project/PROJECT.md)
3. [.specs/project/ROADMAP.md](.specs/project/ROADMAP.md)
4. [.specs/project/STATE.md](.specs/project/STATE.md)
5. [.specs/features/<feature>/spec.md](.specs/features/<feature>/spec.md)
6. [.specs/features/<feature>/design.md](.specs/features/<feature>/design.md)
7. [.specs/features/<feature>/tasks.md](.specs/features/<feature>/tasks.md)
8. [ARCHITECTURE_RULES.md](ARCHITECTURE_RULES.md), apenas se permanecer como documento distinto
9. [docs/routes-guidelines.md](docs/routes-guidelines.md)
10. [docs/error-handling.md](docs/error-handling.md)
11. [docs/persistence-guidelines.md](docs/persistence-guidelines.md)
12. [docs/testing-guidelines.md](docs/testing-guidelines.md)
13. [docs/checklists.md](docs/checklists.md)
14. [README.md](README.md)

## Precedência

Quando houver conflito, use esta ordem de autoridade:

1. Spec da feature ativa em [.specs/features/<feature>/spec.md](.specs/features/<feature>/spec.md)
2. Design e tasks da feature ativa em [.specs/features/<feature>/design.md](.specs/features/<feature>/design.md) e [.specs/features/<feature>/tasks.md](.specs/features/<feature>/tasks.md)
3. Contexto do projeto em [.specs/project/PROJECT.md](.specs/project/PROJECT.md), [.specs/project/ROADMAP.md](.specs/project/ROADMAP.md) e [.specs/project/STATE.md](.specs/project/STATE.md)
4. Instruções globais em [.github/copilot-instructions.md](.github/copilot-instructions.md)
5. [ARCHITECTURE_RULES.md](ARCHITECTURE_RULES.md), apenas se permanecer como documento distinto
6. Guias de domínio em [docs/](docs/)
7. [docs/checklists.md](docs/checklists.md) como apoio operacional
8. [README.md](README.md) apenas para visão humana e onboarding

## Onde cada coisa fica

- Regras globais de comportamento da IA: [.github/copilot-instructions.md](.github/copilot-instructions.md)
- Visão, objetivos e escopo do projeto: [.specs/project/PROJECT.md](.specs/project/PROJECT.md)
- Marcos, fases e evolução: [.specs/project/ROADMAP.md](.specs/project/ROADMAP.md)
- Memória viva do projeto: [.specs/project/STATE.md](.specs/project/STATE.md)
- Requisitos da feature ativa: [.specs/features/<feature>/spec.md](.specs/features/<feature>/spec.md)
- Decisões de implementação da feature ativa: [.specs/features/<feature>/design.md](.specs/features/<feature>/design.md)
- Tarefas atômicas da feature ativa: [.specs/features/<feature>/tasks.md](.specs/features/<feature>/tasks.md)
- Regras de rotas: [docs/routes-guidelines.md](docs/routes-guidelines.md)
- Tratamento de erro: [docs/error-handling.md](docs/error-handling.md)
- Persistência: [docs/persistence-guidelines.md](docs/persistence-guidelines.md)
- Testes: [docs/testing-guidelines.md](docs/testing-guidelines.md)
- Apoio operacional: [docs/checklists.md](docs/checklists.md)
- Visão rápida para pessoas: [README.md](README.md)
- Orientação arquitetural raiz: [ARCHITECTURE_RULES.md](ARCHITECTURE_RULES.md), apenas se permanecer como documento distinto

## Regras de uso

- Não duplicar regra entre raiz, docs e specs.
- Não expandir este arquivo com detalhes de implementação.
- Preferir a spec da feature ativa como fonte de verdade do trabalho atual.
- Preferir os docs de domínio apenas quando a tarefa tocar aquela área.
- Usar [docs/checklists.md](docs/checklists.md) como apoio de execução, não como norma.
- Respeitar Gitflow: `main` para produção, `develop` para integração, `feature/*` para entregas e `hotfix/*` para correções urgentes.
- Respeitar o padrão de commits definido para o repositório.

## Regra prática

Se houver dúvida sobre onde começar, leia nesta ordem:

1. [.specs/project/PROJECT.md](.specs/project/PROJECT.md)
2. [.specs/features/<feature>/spec.md](.specs/features/<feature>/spec.md)
3. [docs/](docs/) apenas para aplicar regras de domínio
