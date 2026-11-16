import unittest

from locomat import create_app


class FluxoDeCadastroPelaWebTest(unittest.TestCase):
    """Fluxo mínimo ponta a ponta: tela -> serviço -> repositório -> banco -> tela."""

    def setUp(self):
        self.cliente = create_app(":memory:").test_client()

    def test_cadastrar_pela_tela_e_ver_na_listagem_e_no_historico(self):
        resp = self.cliente.post("/materiais", data={
            "codigo": "BOLA-001", "nome": "Bola de vôlei",
            "tipo": "esportivo", "conservacao": "bom"}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("BOLA-001", html)
        self.assertIn("Material BOLA-001 cadastrado.", html)

        historico = self.cliente.get("/materiais/BOLA-001/historico").get_data(as_text=True)
        self.assertIn("cadastro", historico)

    def test_cadastro_invalido_mostra_mensagem_e_nao_grava(self):
        resp = self.cliente.post("/materiais", data={
            "codigo": "", "nome": "Bola", "tipo": "esportivo", "conservacao": "bom"},
            follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn("Informe o código do material.", html)
        self.assertIn("Nenhum material cadastrado.", html)


if __name__ == "__main__":
    unittest.main()
