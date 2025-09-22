from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QLabel, QHBoxLayout
from View.NovoClienteDialog import NovoClienteDialog

class ClienteView(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Clientes")
        self.resize(500, 400)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Lista de Clientes:"))

        self.lista_clientes = QListWidget()
        layout.addWidget(self.lista_clientes)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_adicionar = QPushButton("Adicionar Novo Cliente")
        self.btn_editar = QPushButton("Editar Cliente")
        self.btn_apagar = QPushButton("Apagar Cliente")
        btn_layout.addWidget(self.btn_adicionar)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_apagar)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Conectar sinais
        self.btn_adicionar.clicked.connect(self._novo_cliente)
        self.btn_editar.clicked.connect(self._editar_cliente)
        self.btn_apagar.clicked.connect(self._apagar_cliente)

        self._atualizar_lista()

    def _atualizar_lista(self):
        self.lista_clientes.clear()
        clientes = self.controller.listar_clientes()
        for c in clientes:
            self.lista_clientes.addItem(f"{c['id']}: {c['nome']}")

    def _novo_cliente(self):
        dialog = NovoClienteDialog(self.controller)
        if dialog.exec_():
            self._atualizar_lista()

    def _editar_cliente(self):
        item = self.lista_clientes.currentItem()
        if not item:
            QMessageBox.warning(self, "Erro", "Selecione um cliente para editar.")
            return

        cliente_id = int(item.text().split(":")[0])
        cliente = self.controller.obter_cliente_por_id(cliente_id)

        dialog = NovoClienteDialog(self.controller, cliente=cliente)
        if dialog.exec_():
            self._atualizar_lista()

    def _apagar_cliente(self):
        item = self.lista_clientes.currentItem()
        if not item:
            QMessageBox.warning(self, "Erro", "Selecione um cliente para apagar.")
            return

        cliente_id = int(item.text().split(":")[0])
        confirm = QMessageBox.question(
            self,
            "Confirmação",
            "Deseja realmente apagar este cliente?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.controller.remover_cliente(cliente_id)
            self._atualizar_lista()
