# View/CriarOrcamentoDialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QDateEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import QDate
from DAO.ClienteDAO import ClienteDAO
from DAO.VeiculoDAO import VeiculoDAO


class CriarOrcamentoDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Criar Orçamento")
        self.controller = controller

        self.cliente_dao = ClienteDAO()
        self.veiculo_dao = VeiculoDAO()

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Cliente
        layout.addWidget(QLabel("Cliente:"))
        self.combo_cliente = QComboBox()
        layout.addWidget(self.combo_cliente)
        btn_novo_cliente = QPushButton("➕ Criar Novo Cliente")
        btn_novo_cliente.clicked.connect(self._criar_novo_cliente)
        layout.addWidget(btn_novo_cliente)

        # Veículo
        layout.addWidget(QLabel("Veículo:"))
        self.combo_veiculo = QComboBox()
        layout.addWidget(self.combo_veiculo)
        btn_novo_veiculo = QPushButton("➕ Criar Novo Veículo")
        btn_novo_veiculo.clicked.connect(self._criar_novo_veiculo)
        layout.addWidget(btn_novo_veiculo)

        # Descrição
        layout.addWidget(QLabel("Descrição:"))
        self.input_descricao = QLineEdit()
        layout.addWidget(self.input_descricao)

        # Valor estimado
        layout.addWidget(QLabel("Valor Estimado (€):"))
        self.input_valor = QLineEdit()
        layout.addWidget(self.input_valor)

        # Validade
        layout.addWidget(QLabel("Validade:"))
        self.input_validade = QDateEdit()
        self.input_validade.setDate(QDate.currentDate().addDays(30))
        self.input_validade.setCalendarPopup(True)
        layout.addWidget(self.input_validade)

        # Estado
        layout.addWidget(QLabel("Estado:"))
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["pendente", "aprovado", "rejeitado"])
        layout.addWidget(self.combo_estado)

        # Botões
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self._salvar_orcamento)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _load_data(self):
        """Carrega clientes e veículos da BD"""
        self.combo_cliente.clear()
        clientes = self.cliente_dao.listar_clientes()
        for c in clientes:
            self.combo_cliente.addItem(c["nome"], c["id"])

        self._load_veiculos()

    def _load_veiculos(self, cliente_id=None):
        self.combo_veiculo.clear()
        cliente_id = cliente_id or self.combo_cliente.currentData()
        veiculos = self.veiculo_dao.listar_por_cliente(cliente_id)
        for v in veiculos:
            self.combo_veiculo.addItem(f"{v['marca']} {v['modelo']} - {v['matricula']}", v["id"])

    def _criar_novo_cliente(self):
        from View.NovoClienteDialog import NovoClienteDialog
        dialog = NovoClienteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self._load_data()

    def _criar_novo_veiculo(self):
        from View.NovoVeiculoDialog import NovoVeiculoDialog
        cliente_id = self.combo_cliente.currentData()
        dialog = NovoVeiculoDialog(cliente_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self._load_veiculos(cliente_id)

    def _salvar_orcamento(self):
        cliente_id = self.combo_cliente.currentData()
        veiculo_id = self.combo_veiculo.currentData()
        descricao = self.input_descricao.text().strip()
        valor = self.input_valor.text().strip()
        validade = self.input_validade.date().toPyDate()
        estado = self.combo_estado.currentText()

        if not cliente_id or not veiculo_id or not valor:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            valor = float(valor)
        except ValueError:
            QMessageBox.warning(self, "Erro", "O valor estimado deve ser numérico.")
            return

        self.controller.criar_orcamento(
            cliente_id, veiculo_id, descricao, valor, validade, estado
        )
        self.accept()
