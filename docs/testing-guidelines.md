# testing guidelines – api de pesquisa em clima

estas diretrizes definem como escrever testes automatizados neste projeto usando pytest e fastapi.

## 1. objetivos

- garantir que endpoints principais tenham cobertura mínima (health, clima, cidades, histórico, série).
- evitar que a ia “apague” ou quebre testes para fazer o código passar.
- ter um padrão simples e repetível de testes para a própria ia seguir.

## 2. estrutura de testes

- diretório raiz de testes: `tests/`
- arquivos esperados (mínimo):
  - `tests/test_health.py`
  - `tests/test_clima.py`
  - `tests/test_cidades.py`
  - `tests/test_historico.py`
  - `tests/test_serie.py` (se o endpoint existir)

cada arquivo deve focar apenas no seu dom