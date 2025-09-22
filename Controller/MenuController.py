from PyQt5.QtWidgets import QMessageBox
from View.MenuView import MenuView
from DAO.UtilizadorDAO import UtilizadorDAO
from Controller.ClienteController import ClienteController
from Controller.VeiculoController import VeiculoController
from Controller.OrcamentoController import OrcamentoController
from DAO.OrcamentoDAO import OrcamentoDAO  # Certifique-se de importar corretamente o DAO

class MenuController:
    def __init__(self, username: str):
        """
        Inicializa o controlador do menu. A vista (view) do menu será criada aqui.
        """
        self.dao = UtilizadorDAO()
        self.utilizador = self.dao.obter_utilizador(username)

        if not self.utilizador:
            QMessageBox.critical(None, "Erro", f"Utilizador '{username}' não encontrado.")
            return

        # Criação da vista (MenuView) e configuração da interface
        self.view = MenuView()  # Passa apenas o 'parent' (None) para o QMainWindow
        self.view.set_utilizador(self.utilizador)  # Passa o utilizador para a view

        # Ligar os botões aos métodos
        self.view.btn_orcamentos.clicked.connect(self.abrir_orcamentos)
        self.view.btn_folhas_servico.clicked.connect(self.abrir_folhas_servico)
        self.view.btn_clientes.clicked.connect(self.abrir_clientes)
        self.view.btn_veiculos.clicked.connect(self.abrir_veiculos)

        # Configurar permissões com base no papel (role) do utilizador
        self._configurar_permissoes()

    def _configurar_permissoes(self):
        """
        Configura as permissões dos botões com base no papel do utilizador.
        """
        if self.utilizador.role == "funcionario":
            # Desabilitar botões que não são permitidos para funcionários
            self.view.btn_orcamentos.setEnabled(False)
            self.view.btn_clientes.setEnabled(False)
            self.view.btn_veiculos.setEnabled(False)
        else:
            # Habilitar todos os botões se o utilizador for administrador
            self.view.btn_orcamentos.setEnabled(True)
            self.view.btn_clientes.setEnabled(True)
            self.view.btn_veiculos.setEnabled(True)

    def abrir_clientes(self):
        """
        Abre a interface para gerir clientes.
        """
        cliente_controller = ClienteController()
        cliente_controller.iniciar()

    def abrir_veiculos(self):
        """
        Abre a interface para gerir veículos.
        """
        veiculo_controller = VeiculoController()
        veiculo_controller.iniciar()

    def abrir_orcamentos(self):
        """
        Abre a interface para gerir orçamentos. Somente administradores têm permissão.
        """
        if self.utilizador.role != "admin":
            QMessageBox.warning(self.view, "Permissão negada", "Apenas administradores podem gerir orçamentos.")
            return

        # Criando a instância do OrcamentoDAO e passando para o OrcamentoController
        orcamento_dao = OrcamentoDAO()  # Instancia o DAO
        orcamento_controller = OrcamentoController(orcamento_dao)  # Passa o DAO para o controlador de orçamentos
        orcamento_controller.iniciar()  # Inicia o controlador de orçamentos

    def abrir_folhas_servico(self):
        """
        Lógica para abrir o controlador de folhas de serviço (não implementado aqui).
        """
        pass

    def iniciar(self):
        """
        Exibe a interface do menu.
        """
        self.view.show()
