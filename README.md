# LocoMat

Controle de empréstimo, reserva e manutenção de materiais da Atlética Loucomotiva (UFOP/ICEA).
Projeto da disciplina CSI410, Engenharia de Software II, 2026/2. Grupo: Rany Souza, Marco Antonio e Weder Souza.

Esta é a **Etapa 2**: um esqueleto executável de um monolito modular em Python que atravessa todas as
partes da arquitetura (tela, serviço, repositório, banco), com testes e integração contínua.
Ainda não há funcionalidades completas do cliente; o fluxo mínimo é cadastrar e consultar materiais,
com o movimento de cadastro gravado no histórico.

## Como executar

Requisitos: Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app locomat run          # abre em http://127.0.0.1:5000
```

Com Docker: `docker compose up --build` (o banco SQLite fica no volume `locomat-dados`).

## Como testar

```bash
python -m unittest discover -s tests -v
```

Os testes incluem `tests/test_regras_dependencia.py`, que verifica as regras de dependência entre os módulos.

## Estrutura (espelha a visão de módulos do documento de arquitetura)

| Pasta | Segredo (o que o módulo esconde) |
|---|---|
| `locomat/web` | o framework web e como as telas são montadas |
| `locomat/materiais` | o ciclo do material (estados e transições permitidas) |
| `locomat/historico` | como os movimentos são gravados e consultados |
| `locomat/persistencia` | qual banco é usado e como as tabelas são organizadas |
| `locomat/emprestimos` (Etapa 3) | como o prazo padrão e o atraso são calculados |
| `locomat/reservas` (Etapa 3) | como a sobreposição de reservas é impedida |
| `locomat/manutencao` (Etapa 3) | como o dano e o reparo são registrados |
| `locomat/acesso` (Etapa 3) | como os responsáveis autorizados são identificados |

`locomat/__init__.py` é a raiz de composição: o único ponto que liga web, serviços e persistência.

## Fluxo de trabalho

- `main` só recebe mudanças por pull request, revisado por outro integrante, com o pipeline passando.
- Uma branch por história (ex.: `h03-registrar-emprestimo`).
- O pipeline (`.github/workflows/ci.yml`) roda build e testes a cada push e pull request.
- A entrega da Etapa 2 está marcada com a tag `etapa-2`.
