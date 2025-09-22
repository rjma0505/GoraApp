from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QMessageBox
from Model.Cliente import Cliente

class NovoClienteDialog(QDialog):
    def __init__(self, controller, cliente=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.cliente = cliente
        self.setWindowTitle("Novo Cliente" if cliente is None else "Editar Cliente")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.input_nome = QLineEdit()
        self.input_contacto = QLineEdit()
        self.input_email = QLineEdit()
        self.input_morada = QLineEdit()

        if cliente:
            self.input_nome.setText(cliente.nome)
            self.input_contacto.setText(cliente.contacto or "")
            self.input_email.setText(cliente.email or "")
            self.input_morada.setText(cliente.morada or "")

        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(self.input_nome)
        layout.addWidget(QLabel("Contacto:"))
        layout.addWidget(self.input_contacto)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.input_email)
        layout.addWidget(QLabel("Morada:"))
        layout.addWidget(self.input_morada)

        btn_layout = QHBoxLayout()
        self.btn_salvar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_cancelar)
        layout.addLayout(btn_layout)

        self.btn_salvar.clicked.connect(self._salvar)
        self.btn_cancelar.clicked.connect(self.reject)
        self.setLayout(layout)

    def _salvar(self):
        nome = self.input_nome.text().strip()
        contacto = self.input_contacto.text().strip()
        email = self.input_email.text().strip()
        morada = self.input_morada.text().strip()

        if not nome:
            QMessageBox.warning(self, "Erro", "O nome é obrigatório.")
            return

        if self.cliente:
            self.cliente.nome = nome
            self.cliente.contacto = contacto
            self.cliente.email = email
            self.cliente.morada = morada
            self.controller.atualizar_cliente(self.cliente)
        else:
            cliente = Cliente(nome=nome, contacto=contacto, email=email, morada=morada)
            self.controller.adicionar_cliente(cliente)

        self.accept()
