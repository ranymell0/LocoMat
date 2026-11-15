"""Verifica as regras de dependência do documento de arquitetura (Etapa 2, seção 6).

R1  Módulos de domínio não importam flask, sqlite3, locomat.web nem locomat.persistencia.
R2  A web não importa locomat.persistencia.
R3  A persistência não importa locomat.web.
R4  Um módulo só usa outro pela interface pública do pacote (from locomat.outro import X).
R5  Só existem as dependências permitidas entre módulos (sem ciclos).
"""
import ast
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "locomat"
DOMINIO = {"acesso", "materiais", "historico", "emprestimos", "reservas", "manutencao"}
INFRA_PROIBIDA_NO_DOMINIO = {"flask", "sqlite3", "werkzeug", "jinja2"}
PERMITIDAS = {
    "historico": set(),
    "acesso": set(),
    "materiais": {"historico"},
    "emprestimos": {"materiais", "historico"},
    "reservas": {"materiais", "historico"},
    "manutencao": {"materiais", "historico"},
    "web": DOMINIO,
    "persistencia": DOMINIO,
}


def importacoes(arquivo: Path):
    """Devolve os nomes absolutos importados (imports relativos são internos ao módulo)."""
    arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            for alias in no.names:
                yield alias.name
        elif isinstance(no, ast.ImportFrom) and no.level == 0 and no.module:
            yield no.module


def arquivos_por_modulo():
    for pasta in sorted(p for p in RAIZ.iterdir() if p.is_dir() and not p.name.startswith("__")):
        for arquivo in pasta.rglob("*.py"):
            yield pasta.name, arquivo


class RegrasDeDependenciaTest(unittest.TestCase):
    def test_modulos_esperados_existem(self):
        existentes = {p.name for p in RAIZ.iterdir() if p.is_dir() and not p.name.startswith("__")}
        self.assertEqual(existentes, set(PERMITIDAS))

    def test_dominio_nao_depende_de_infraestrutura(self):  # R1
        for modulo, arquivo in arquivos_por_modulo():
            if modulo not in DOMINIO:
                continue
            for nome in importacoes(arquivo):
                with self.subTest(arquivo=arquivo.name, importa=nome):
                    self.assertNotIn(nome.split(".")[0], INFRA_PROIBIDA_NO_DOMINIO)
                    self.assertFalse(nome.startswith(("locomat.web", "locomat.persistencia")))

    def test_web_nao_importa_persistencia_e_vice_versa(self):  # R2 e R3
        for modulo, arquivo in arquivos_por_modulo():
            for nome in importacoes(arquivo):
                with self.subTest(arquivo=arquivo.name, importa=nome):
                    if modulo == "web":
                        self.assertFalse(nome.startswith("locomat.persistencia"))
                    if modulo == "persistencia":
                        self.assertFalse(nome.startswith("locomat.web"))

    def test_modulos_so_se_usam_pela_interface_publica(self):  # R4
        for modulo, arquivo in arquivos_por_modulo():
            for nome in importacoes(arquivo):
                partes = nome.split(".")
                if partes[0] == "locomat" and len(partes) > 1 and partes[1] != modulo:
                    with self.subTest(arquivo=arquivo.name, importa=nome):
                        self.assertEqual(len(partes), 2, "use 'from locomat.<modulo> import ...'")

    def test_so_ha_dependencias_permitidas(self):  # R5
        for modulo, arquivo in arquivos_por_modulo():
            for nome in importacoes(arquivo):
                partes = nome.split(".")
                if partes[0] == "locomat" and len(partes) > 1 and partes[1] != modulo:
                    with self.subTest(arquivo=arquivo.name, importa=nome):
                        self.assertIn(partes[1], PERMITIDAS[modulo])


if __name__ == "__main__":
    unittest.main()
