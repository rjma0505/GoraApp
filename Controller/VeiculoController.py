# Controller/VeiculoController.py
from DAO.VeiculoDAO import VeiculoDAO
from DAO.ClienteDAO import ClienteDAO
from View.VeiculoView import VeiculoView
from View.NovoVeiculoDialog import NovoVeiculoDialog
from Model.Veiculo import Veiculo

class VeiculoController:
    def __init__(self):
        self.dao = VeiculoDAO()
        self.cliente_dao = ClienteDAO()
        self.clientes = self.cliente_dao.listar_clientes()
        self.view = VeiculoView(self.clientes)

        self.view.btn_criar.clicked.connect(self.adicionar_veiculo)
        self.view.btn_editar.clicked.connect(self.editar_veiculo)
        self.view.btn_apagar.clicked.connect(self.apagar_veiculo)

    def iniciar(self):
        self.atualizar_lista_veiculos()
        self.view.exec_()

    def atualizar_lista_veiculos(self):
        veiculos = self.dao.listar_todos_veiculos()
        self.view.popular_lista(veiculos)

    def adicionar_veiculo(self):
        dialog = NovoVeiculoDialog()
        if dialog.exec_():
            self.atualizar_lista_veiculos()

    def editar_veiculo(self):
        veiculo_id = self.view.obter_veiculo_selecionado_id()
        if not veiculo_id:
            self.view.mostrar_mensagem("Erro", "Selecione um veículo para editar.")
            return
        veiculo = self.dao.obter_veiculo_por_id(veiculo_id)
        if not veiculo:
            self.view.mostrar_mensagem("Erro", "Veículo não encontrado.")
            return

        dialog = NovoVeiculoDialog()
        dialog.combo_cliente.setCurrentIndex(
            next(i for i, c in enumerate(dialog.clientes) if c['id'] == veiculo.cliente_id)
        )
        dialog.input_marca.setText(veiculo.marca)
        dialog.input_modelo.setText(veiculo.modelo)
        dialog.input_matricula.setText(veiculo.matricula)
        dialog.combo_pais.setCurrentText(veiculo.pais)

        if dialog.exec_():
            dados = dialog
            veiculo.cliente_id = dialog.combo_cliente.currentData()
            veiculo.marca = dialog.input_marca.text()
            veiculo.modelo = dialog.input_modelo.text()
            veiculo.matricula = dialog.input_matricula.text()
            veiculo.pais = dialog.combo_pais.currentText()
            self.dao.atualizar_veiculo(veiculo)
            self.atualizar_lista_veiculos()

    def apagar_veiculo(self):
        veiculo_id = self.view.obter_veiculo_selecionado_id()
        if not veiculo_id:
            self.view.mostrar_mensagem("Erro", "Selecione um veículo para apagar.")
            return
        self.dao.eliminar_veiculo(veiculo_id)
        self.atualizar_lista_veiculos()
