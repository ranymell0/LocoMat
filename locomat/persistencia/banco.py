import sqlite3
import threading
from contextlib import contextmanager

ESQUEMA = """
CREATE TABLE IF NOT EXISTS material (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    conservacao TEXT NOT NULL,
    estado TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS movimento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_codigo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    responsavel TEXT,
    registrado_por TEXT NOT NULL,
    estado_resultante TEXT NOT NULL,
    registrado_em TEXT NOT NULL
);
"""


class Banco:
    """Conexão única com transação explícita e reentrante (só a mais externa confirma)."""

    def __init__(self, caminho: str):
        self.conexao = sqlite3.connect(caminho, check_same_thread=False, isolation_level=None)
        self.conexao.row_factory = sqlite3.Row
        self._trava = threading.RLock()
        self._profundidade = 0

    def criar_esquema(self) -> None:
        with self._trava:
            self.conexao.executescript(ESQUEMA)

    @contextmanager
    def transacao(self):
        with self._trava:
            if self._profundidade == 0:
                self.conexao.execute("BEGIN IMMEDIATE")
            self._profundidade += 1
            try:
                yield self.conexao
            except BaseException:
                self._profundidade -= 1
                if self._profundidade == 0:
                    self.conexao.execute("ROLLBACK")
                raise
            else:
                self._profundidade -= 1
                if self._profundidade == 0:
                    self.conexao.execute("COMMIT")

    def executar(self, sql: str, parametros: tuple = ()):
        with self._trava:
            return self.conexao.execute(sql, parametros)
