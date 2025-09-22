# Controller/ClienteController.py

from DAO.ClienteDAO import ClienteDAO
from View.ClienteView import ClienteView
from Model.Cliente import Cliente

class ClienteController:
    def __init__(self):
        self.dao = ClienteDAO()  # Instância da DAO de Cliente

    def iniciar(self):
        """Inicia o processo de adição de cliente"""
        cliente_view = ClienteView(self)  # Passa o controlador para a view
        cliente_view.exec_()

    def adicionar_cliente(self, nome, contacto, email, morada, criado_em):
        """Adiciona um cliente no banco de dados"""
        cliente = Cliente(nome, contacto, email, morada, criado_em)  # Cria um objeto Cliente
        self.dao.adicionar_cliente(cliente)  # Chama a DAO para salvar o cliente no banco de dados
