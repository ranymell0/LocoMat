import unittest
from datetime import datetime, timezone

from locomat.historico import HistoricoService
from locomat.materiais import CodigoDuplicado, EstadoMaterial, MaterialInvalido, MaterialService
from locomat.persistencia import Banco, RepositorioHistoricoSQL, RepositorioMateriaisSQL


def montar(relogio=None):
    banco = Banco(":memory:")
    banco.criar_esquema()
    historico = HistoricoService(RepositorioHistoricoSQL(banco),
                                 relogio or (lambda: datetime(2026, 11, 20, 10, 0, tzinfo=timezone.utc)))
    servico = MaterialService(RepositorioMateriaisSQL(banco), historico, banco.transacao)
    return banco, servico, historico


class CadastroDeMaterialTest(unittest.TestCase):
    def test_cadastra_e_lista_como_disponivel(self):  # H01 e H02
        _, servico, _ = montar()
        servico.cadastrar("bola-001", "Bola de vôlei", "esportivo", "bom")
        itens = servico.listar()
        self.assertEqual([m.codigo for m in itens], ["BOLA-001"])
        self.assertEqual(itens[0].estado, EstadoMaterial.DISPONIVEL)

    def test_recusa_campo_obrigatorio_vazio(self):
        _, servico, _ = montar()
        with self.assertRaises(MaterialInvalido):
            servico.cadastrar("", "Bola", "esportivo", "bom")
        with self.assertRaises(MaterialInvalido):
            servico.cadastrar("BOLA-001", "  ", "esportivo", "bom")
        self.assertEqual(servico.listar(), [])

    def test_recusa_codigo_duplicado(self):
        _, servico, _ = montar()
        servico.cadastrar("SURDO-01", "Surdo", "instrumento_bateria", "bom")
        with self.assertRaises(CodigoDuplicado):
            servico.cadastrar("surdo-01", "Outro surdo", "instrumento_bateria", "bom")



class RastreabilidadeTest(unittest.TestCase):  # cenário C04
    def test_se_o_historico_falha_o_material_nao_e_gravado(self):
        banco, servico, historico = montar()

        def falhar(*args, **kwargs):
            raise RuntimeError("falha simulada")

        historico.registrar = falhar
        with self.assertRaises(RuntimeError):
            servico.cadastrar("BOLA-001", "Bola", "esportivo", "bom")
        self.assertEqual(servico.listar(), [])
        self.assertEqual(banco.executar("SELECT COUNT(*) FROM material").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
