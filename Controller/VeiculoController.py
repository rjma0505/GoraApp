from View.VeiculoView import VeiculoView
from DAO import VeiculoDAO
from Model.Veiculo import Veiculo
from PyQt5.QtWidgets import QMessageBox
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VeiculoController:
    def __init__(self):
        self.view = VeiculoView()
        self.dao = VeiculoDAO()
        self.view.btn_criar.clicked.connect(self.adicionar_veiculo)
        self.view.btn_editar.clicked.connect(self.editar_veiculo)
        self.view.btn_apagar.clicked.connect(self.apagar_veiculo)
        self.view.lista_veiculos.itemClicked.connect(self.preencher_formulario)

    def iniciar(self):
        """Inicia a visualização e carrega os veículos"""
        self.atualizar_lista_veiculos()
        self.view.exec_()

    def atualizar_lista_veiculos(self, cliente_id=None):
        """Atualiza a lista de veículos na interface"""
        veiculos = self.dao.obter_veiculos_por_cliente(cliente_id) if cliente_id else self.dao.obter_todos_veiculos()
        self.view.popular_lista(veiculos)

    def verificar_cliente_id(self, cliente_id_str):
        """Valida o ID do cliente, garantindo que é um número inteiro positivo"""
        try:
            cliente_id = int(cliente_id_str)
            if cliente_id <= 0:
                raise ValueError("O ID do cliente deve ser um número positivo.")
            return cliente_id
        except ValueError as ve:
            self.view.mostrar_mensagem("Erro", str(ve))
            logging.error(f"ID de cliente inválido: {cliente_id_str}")
            return None

    def adicionar_veiculo(self):
        """Adiciona um novo veículo"""
        dados = self.view.obter_dados_formulario()
        cliente_id = self.verificar_cliente_id(dados['cliente_id'])
        if cliente_id:
            novo_veiculo = Veiculo(cliente_id=cliente_id, marca=dados['marca'], modelo=dados['modelo'], matricula=dados['matricula'], pais=dados['pais'])
            if self.dao.criar_veiculo(novo_veiculo):
                self.view.mostrar_mensagem("Sucesso", "Veículo adicionado com sucesso.")
                self.view.limpar_formulario()
                self.atualizar_lista_veiculos(cliente_id)
                logging.info(f"Veículo adicionado: {novo_veiculo}")
            else:
                self.view.mostrar_mensagem("Erro", "Falha ao adicionar veículo.")
                logging.error(f"Falha ao adicionar veículo: {novo_veiculo}")

    def editar_veiculo(self):
        """Edita um veículo existente"""
        veiculo_id = self.view.obter_veiculo_selecionado_id()
        if veiculo_id:
            dados = self.view.obter_dados_formulario()
            cliente_id = self.verificar_cliente_id(dados['cliente_id'])
            if cliente_id:
                veiculo_a_editar = Veiculo(id=veiculo_id, cliente_id=cliente_id, marca=dados['marca'], modelo=dados['modelo'], matricula=dados['matricula'], pais=dados['pais'])
                if self.dao.atualizar_veiculo(veiculo_a_editar):
                    self.view.mostrar_mensagem("Sucesso", "Veículo atualizado com sucesso.")
                    self.view.limpar_formulario()
                    self.atualizar_lista_veiculos(cliente_id)
                    logging.info(f"Veículo atualizado: {veiculo_a_editar}")
                else:
                    self.view.mostrar_mensagem("Erro", "Falha ao atualizar veículo.")
                    logging.error(f"Falha ao atualizar veículo: {veiculo_a_editar}")
        else:
            self.view.mostrar_mensagem("Erro", "Selecione um veículo para editar.")

    def apagar_veiculo(self):
        """Apaga um veículo"""
        veiculo_id = self.view.obter_veiculo_selecionado_id()
        if veiculo_id:
            confirmar = QMessageBox.question(self.view, 'Confirmação', "Tem certeza que deseja apagar este veículo?", QMessageBox.Yes | QMessageBox.No)
            if confirmar == QMessageBox.Yes:
                if self.dao.excluir_veiculo(veiculo_id):
                    self.view.mostrar_mensagem("Sucesso", "Veículo apagado com sucesso.")
                    self.atualizar_lista_veiculos()
                    logging.info(f"Veículo ID {veiculo_id} apagado com sucesso.")
                else:
                    self.view.mostrar_mensagem("Erro", "Falha ao apagar veículo.")
                    logging.error(f"Falha ao apagar o veículo ID: {veiculo_id}")
        else:
            self.view.mostrar_mensagem("Erro", "Selecione um veículo para apagar.")

    def preencher_formulario(self):
        """Preenche o formulário com os dados do veículo selecionado"""
        veiculo_id = self.view.obter_veiculo_selecionado_id()
        if veiculo_id:
            veiculo = self.dao.obter_veiculo_por_id(veiculo_id)
            if veiculo:
                self.view.input_cliente_id.setText(str(veiculo.cliente_id))
                self.view.input_marca.setText(veiculo.marca)
                self.view.input_modelo.setText(veiculo.modelo)
                self.view.input_matricula.setText(veiculo.matricula)
                self.view.input_pais.setText(veiculo.pais)
                logging.info(f"Formulário preenchido com os dados do veículo ID: {veiculo_id}")
            else:
                self.view.mostrar_mensagem("Erro", "Veículo não encontrado.")
                logging.error(f"Veículo ID {veiculo_id} não encontrado.")
