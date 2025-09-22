from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from DAO.UtilizadorDAO import UtilizadorDAO  # Certifique-se de que o caminho esteja correto
import bcrypt

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 150)

        # Layout principal
        layout = QVBoxLayout()

        # Criação dos widgets
        self.lbl_user = QLabel("Username:")
        self.txt_user = QLineEdit()
        self.lbl_pass = QLabel("Password:")
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.btn_login = QPushButton("Entrar")

        # Adicionando os widgets ao layout
        layout.addWidget(self.lbl_user)
        layout.addWidget(self.txt_user)
        layout.addWidget(self.lbl_pass)
        layout.addWidget(self.txt_pass)
        layout.addWidget(self.btn_login)

        # Conectando o botão a um slot
        self.btn_login.clicked.connect(self.on_login)

        # Definindo o layout da janela
        self.setLayout(layout)

        # Inicializando o DAO para autenticação
        self.utilizador_dao = UtilizadorDAO()

    def on_login(self):
        """Método que será chamado ao clicar no botão de login."""
        username = self.txt_user.text()
        password = self.txt_pass.text()

        # Validação simples dos campos
        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha ambos os campos.", QMessageBox.Ok)
            return

        # Tenta autenticar usando o DAO
        if self.authenticate(username, password):
            self.accept_login()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.", QMessageBox.Ok)

    def authenticate(self, username, password):
        """Método de autenticação com verificação no banco de dados."""
        try:
            # Obter o utilizador do banco de dados
            utilizador = self.utilizador_dao.obter_utilizador(username)
            
            if utilizador:
                # Verifica a senha fornecida com o hash armazenado
                if bcrypt.checkpw(password.encode('utf-8'), utilizador.password_hash.encode('utf-8')):
                    return True
            return False
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao verificar credenciais: {str(e)}", QMessageBox.Ok)
            return False

    def accept_login(self):
        """Se o login for bem-sucedido, fecha a janela de login ou exibe a próxima tela."""
        self.close()  # Fecha a janela de login
        print("Login bem-sucedido!")
        # Aqui você pode abrir a próxima janela (por exemplo, Menu)
        # menu_view = MenuView()
        # menu_view.show()  # Exibe a próxima janela
