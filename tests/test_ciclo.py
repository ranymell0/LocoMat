import unittest

from locomat.materiais import EstadoMaterial as E
from locomat.materiais import pode_transitar


class CicloDoMaterialTest(unittest.TestCase):  # RN03 e RN05
    def test_disponivel_pode_ser_emprestado(self):
        self.assertTrue(pode_transitar(E.DISPONIVEL, E.EMPRESTADO))

    def test_emprestado_nao_pode_ser_emprestado_de_novo(self):
        self.assertFalse(pode_transitar(E.EMPRESTADO, E.EMPRESTADO))

    def test_material_em_manutencao_so_volta_a_disponivel(self):
        self.assertFalse(pode_transitar(E.EM_MANUTENCAO, E.EMPRESTADO))
        self.assertFalse(pode_transitar(E.EM_MANUTENCAO, E.RESERVADO))
        self.assertTrue(pode_transitar(E.EM_MANUTENCAO, E.DISPONIVEL))


if __name__ == "__main__":
    unittest.main()
