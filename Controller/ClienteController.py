from DAO.ClienteDAO import ClienteDAO
from Model.Cliente import Cliente
from View.ClienteView import ClienteView
from View.NovoClienteDialog import NovoClienteDialog

class ClienteController:
    def __init__(self):
        self.dao = ClienteDAO()

    def iniciar(self):
        """Abre a view de clientes e decide se abre lista ou novo cliente"""
        clientes = self.listar_clientes()
        cliente_view = ClienteView(self)
        cliente_view.exec_()

    # ======== Métodos usados pela view ========
    def listar_clientes(self):
        """Retorna todos os clientes como lista de dicionários"""
        return self.dao.listar_clientes()

    def adicionar_cliente(self, cliente: Cliente):
        self.dao.adicionar_cliente(cliente)

    def obter_cliente_por_id(self, cliente_id: int) -> Cliente:
        return self.dao.obter_cliente_por_id(cliente_id)

    def atualizar_cliente(self, cliente: Cliente):
        self.dao.atualizar_cliente(cliente)

    def remover_cliente(self, cliente_id: int):
        self.dao.remover_cliente(cliente_id)
