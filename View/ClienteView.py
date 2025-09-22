# View/ClienteView.py

from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class ClienteView(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Novo Cliente")
        
        # Layout do formulário
        layout = QFormLayout()
        
        # Campos de dados
        self.nome_input = QLineEdit()
        self.contacto_input = QLineEdit()
        self.email_input = QLineEdit()
        self.morada_input = QLineEdit()
        
        # Adiciona os campos ao formulário
        layout.addRow("Nome:", self.nome_input)
        layout.addRow("Contacto:", self.contacto_input)
        layout.addRow("E-mail:", self.email_input)
        layout.addRow("Morada:", self.morada_input)
        
        # Botões de ação (OK/Cancelar)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.aceitar)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        self.controller = controller  # Controlador passado

    def obter_dados_formulario(self):
        """Obtém os dados inseridos no formulário"""
        nome = self.nome_input.text()
        contacto = self.contacto_input.text()
        email = self.email_input.text()
        morada = self.morada_input.text()
        criado_em = "CURRENT_TIMESTAMP"  # Para a data e hora atual
        
        return nome, contacto, email, morada, criado_em

    def aceitar(self):
        """Ação para adicionar um novo cliente"""
        nome, contacto, email, morada, criado_em = self.obter_dados_formulario()
        
        # Aqui você vai enviar esses dados para o controlador que irá persistir no banco
        self.controller.adicionar_cliente(nome, contacto, email, morada, criado_em)
        
        # Fecha o diálogo após salvar
        self.accept()
