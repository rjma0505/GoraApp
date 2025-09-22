# View/CriarOrcamentoDialog.py

from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox
from Model.Orcamento import Orcamento  # Certifique-se de importar o modelo Orcamento

class CriarOrcamentoDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Criar Novo Orçamento")
        
        self.controller = controller  # Passa o controlador para manipular a criação do orçamento
        
        # Layout do formulário
        layout = QFormLayout()
        
        self.cliente_id_input = QLineEdit()
        self.veiculo_id_input = QLineEdit()
        self.descricao_input = QLineEdit()
        self.valor_estimado_input = QLineEdit()
        self.validade_input = QLineEdit()
        self.estado_input = QLineEdit()
        
        layout.addRow("Cliente ID:", self.cliente_id_input)
        layout.addRow("Veículo ID:", self.veiculo_id_input)
        layout.addRow("Descrição:", self.descricao_input)
        layout.addRow("Valor Estimado:", self.valor_estimado_input)
        layout.addRow("Validade:", self.validade_input)
        layout.addRow("Estado:", self.estado_input)
        
        # Botões de ação (OK/Cancelar)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.aceitar)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def aceitar(self):
        """Ação para criar o orçamento"""
        cliente_id = int(self.cliente_id_input.text())
        veiculo_id = int(self.veiculo_id_input.text())
        descricao = self.descricao_input.text()
        valor_estimado = float(self.valor_estimado_input.text()) if self.valor_estimado_input.text() else 0.0
        validade = self.validade_input.text()  # Pode ser convertida para o tipo de data conforme necessário
        estado = self.estado_input.text()

        # Chama o método criar_orcamento do controlador para criar o orçamento
        self.controller.criar_orcamento(cliente_id, veiculo_id, descricao, valor_estimado, validade, estado)

        # Fecha o diálogo após salvar
        self.accept()
