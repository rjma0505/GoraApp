# Controller/MenuController.py

import sys
from PyQt5.QtWidgets import QMessageBox
from View.MenuView import MenuView
from DAO.UtilizadorDAO import UtilizadorDAO
from Controller.ClienteController import ClienteController
from Controller.VeiculoController import VeiculoController
from Controller.OrcamentoController import OrcamentoController

ROLE_PERMISSOES = {
    "admin": ["orcamentos", "clientes", "veiculos", "folhas"],
    "funcionario": ["folhas"],
}

class MenuController:
    def __init__(self, username: str):
        self.dao = UtilizadorDAO()
        self.utilizador = self.dao.obter_utilizador(username)

        if not self.utilizador:
            QMessageBox.critical(None, "Erro", f"Utilizador '{username}' não encontrado.")
            sys.exit(1)

        self.view = MenuView()
        self.view.set_utilizador(self.utilizador)

        # Liga sinais
        self.view.btn_orcamentos.clicked.connect(self.abrir_orcamentos)
        self.view.btn_folhas_servico.clicked.connect(self.abrir_folhas_servico)
        self.view.btn_clientes.clicked.connect(self.abrir_clientes)
        self.view.btn_veiculos.clicked.connect(self.abrir_veiculos)

        self._configurar_permissoes()

    def _configurar_permissoes(self):
        permissoes = ROLE_PERMISSOES.get(self.utilizador.role, [])
        self.view.btn_orcamentos.setEnabled("orcamentos" in permissoes)
        self.view.btn_clientes.setEnabled("clientes" in permissoes)
        self.view.btn_veiculos.setEnabled("veiculos" in permissoes)
        self.view.btn_folhas_servico.setEnabled("folhas" in permissoes)

    def abrir_clientes(self):
        cliente_controller = ClienteController()
        cliente_controller.iniciar()  # Ele decide qual view abrir

    def abrir_veiculos(self):
        veiculo_controller = VeiculoController()
        veiculo_controller.iniciar()

    def abrir_orcamentos(self):
        if self.utilizador.role != "admin":
            QMessageBox.warning(self.view, "Permissão negada", "Apenas administradores podem gerir orçamentos.")
            return
        # Corrigido: instanciando OrcamentoController sem argumentos
        orcamento_controller = OrcamentoController()
        orcamento_controller.iniciar()

    def abrir_folhas_servico(self):
        QMessageBox.information(self.view, "Folhas de Serviço", "Funcionalidade ainda não implementada.")

    def iniciar(self):
        self.view.show()
