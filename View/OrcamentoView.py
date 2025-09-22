# View/OrcamentoView.py

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from View.CriarOrcamentoDialog import CriarOrcamentoDialog

class OrcamentoView(QMainWindow):
    def __init__(self, orcamentos, controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Orçamentos")
        self.setMinimumSize(1300, 500)  # Maior largura para caber a coluna de descrição
        self.orcamentos = orcamentos
        self.controller = controller

        layout = QVBoxLayout()

        # Tabela de orçamentos
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Cliente", "Veículo", "Descrição", "Valor Estimado", "Estado", "Data Criação", "Validade"
        ])
        self.table.setRowCount(len(orcamentos))
        self.table.setWordWrap(True)
        self.table.setAlternatingRowColors(True)

        # Preencher a tabela
        for row, o in enumerate(orcamentos):
            self.table.setItem(row, 0, QTableWidgetItem(str(o.id)))
            self.table.setItem(row, 1, QTableWidgetItem(o.cliente_nome))
            self.table.setItem(row, 2, QTableWidgetItem(f"{o.veiculo_marca} {o.veiculo_modelo}"))
            self.table.setItem(row, 3, QTableWidgetItem(o.descricao))
            self.table.setItem(row, 4, QTableWidgetItem(str(o.valor_estimado)))
            self.table.setItem(row, 5, QTableWidgetItem(o.estado))
            self.table.setItem(row, 6, QTableWidgetItem(str(o.data_criacao)))
            self.table.setItem(row, 7, QTableWidgetItem(str(o.validade)))

        # Ajustar largura das colunas
        self.table.setColumnWidth(0, 50)    # ID
        self.table.setColumnWidth(1, 150)   # Cliente
        self.table.setColumnWidth(2, 150)   # Veículo
        self.table.setColumnWidth(3, 450)   # Descrição (maior)
        self.table.setColumnWidth(4, 120)   # Valor Estimado
        self.table.setColumnWidth(5, 100)   # Estado
        self.table.setColumnWidth(6, 150)   # Data Criação
        self.table.setColumnWidth(7, 100)   # Validade (apenas para a data)

        layout.addWidget(self.table)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_novo = QPushButton("Novo Orçamento")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_exportar = QPushButton("Exportar PDF")

        btn_layout.addWidget(self.btn_novo)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_exportar)

        layout.addLayout(btn_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Conexões dos botões
        self.btn_novo.clicked.connect(self._novo_orcamento)
        self.btn_editar.clicked.connect(self._editar_orcamento)
        self.btn_eliminar.clicked.connect(self._eliminar_orcamento)
        self.btn_exportar.clicked.connect(self._exportar_pdf)

    def _get_selected_orcamento(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Erro", "Selecione um orçamento.")
            return None
        return self.orcamentos[row]

    def _novo_orcamento(self):
        dialog = CriarOrcamentoDialog(self.controller)
        dialog.exec_()

    def _editar_orcamento(self):
        o = self._get_selected_orcamento()
        if o:
            dialog = CriarOrcamentoDialog(self.controller, orcamento_id=o.id)
            dialog.exec_()

    def _eliminar_orcamento(self):
        o = self._get_selected_orcamento()
        if o:
            confirm = QMessageBox.question(self, "Confirmar", f"Eliminar orçamento #{o.id}?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.controller.eliminar_orcamento(o.id)

    def _exportar_pdf(self):
        o = self._get_selected_orcamento()
        if o:
            self.controller.exportar_pdf_orcamento(o)

