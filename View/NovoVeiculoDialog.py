# View/NovoVeiculoDialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QMessageBox
from Model.Veiculo import Veiculo
from DAO.VeiculoDAO import VeiculoDAO
from DAO.ClienteDAO import ClienteDAO

class NovoVeiculoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Veículo")
        self.resize(400, 300)

        self.veiculo_dao = VeiculoDAO()
        self.cliente_dao = ClienteDAO()

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Dropdown de clientes
        self.combo_cliente = QComboBox()
        self.clientes = self.cliente_dao.listar_clientes()
        for c in self.clientes:
            self.combo_cliente.addItem(f"{c['nome']} (ID: {c['id']})", c['id'])

        # Campos de texto
        self.input_marca = QLineEdit()
        self.input_modelo = QLineEdit()
        self.input_matricula = QLineEdit()

        # Dropdown de país
        self.combo_pais = QComboBox()
        self.combo_pais.addItems(["Portugal", "Espanha", "França", "Alemanha", "Luxemburgo", "Suíça"])

        # Adiciona ao form
        form_layout.addRow("Cliente:", self.combo_cliente)
        form_layout.addRow("Marca:", self.input_marca)
        form_layout.addRow("Modelo:", self.input_modelo)
        form_layout.addRow("Matrícula:", self.input_matricula)
        form_layout.addRow("País:", self.combo_pais)
        layout.addLayout(form_layout)

        # Botões
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")
        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)

        btn_salvar.clicked.connect(self._salvar)
        btn_cancelar.clicked.connect(self.reject)

        self.setLayout(layout)

    def _salvar(self):
        cliente_id = self.combo_cliente.currentData()
        marca = self.input_marca.text().strip()
        modelo = self.input_modelo.text().strip()
        matricula = self.input_matricula.text().strip()
        pais = self.combo_pais.currentText()

        if not all([cliente_id, marca, modelo, matricula, pais]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        try:
            # Cria o objeto Veiculo; valida matrícula e país no Python
            veiculo = Veiculo(
                cliente_id=cliente_id,
                marca=marca,
                modelo=modelo,
                matricula=matricula,
                pais=pais
            )
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))
            return

        # Adiciona ao banco de dados via DAO
        self.veiculo_dao.criar_veiculo(veiculo)
        QMessageBox.information(self, "Sucesso", f"Veículo {matricula} adicionado com sucesso!")
        self.accept()
