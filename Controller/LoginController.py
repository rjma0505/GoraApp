import bcrypt  # Certifique-se de que o bcrypt está importado
from PyQt5.QtWidgets import QMessageBox
from View.LoginView import LoginView
from Controller.MenuController import MenuController  # Certifique-se de que o MenuController está sendo importado corretamente
from DAO.UtilizadorDAO import UtilizadorDAO  # Certifique-se de que o UtilizadorDAO está sendo importado corretamente

class LoginController:
    def __init__(self):
        self.login_view = LoginView()
        self.utilizador_dao = UtilizadorDAO()
        self.login_view.btn_login.clicked.connect(self.validar_login)

    def iniciar(self):
        self.login_view.show()

    def validar_login(self):
        username = self.login_view.txt_user.text()  # Alterado para txt_user
        password = self.login_view.txt_pass.text()  # Alterado para txt_pass

        # Valida se os campos estão preenchidos
        if not username or not password:
            QMessageBox.warning(self.login_view, "Erro de Login", "Por favor, preencha todos os campos.")
            return

        # Desabilitar o botão de login durante a validação
        self.login_view.btn_login.setEnabled(False)

        # Tenta obter o utilizador no banco de dados
        try:
            utilizador = self.utilizador_dao.obter_utilizador(username)
        except Exception as e:
            QMessageBox.critical(self.login_view, "Erro de Conexão", f"Erro ao acessar o banco de dados: {e}")
            self.login_view.btn_login.setEnabled(True)
            return

        if utilizador and utilizador.verificar_password(password):  # Usando o método verificar_password aqui
            self.login_view.close()  # Fecha a tela de login

            # Cria e exibe o menu
            self.menu_controller = MenuController(utilizador.username)  # Agora passamos apenas o 'username'
            self.menu_controller.iniciar()

            # Opcional: Mensagem de boas-vindas
            QMessageBox.information(self.login_view, "Login Bem-Sucedido", f"Bem-vindo, {utilizador.nome}!")
        else:
            QMessageBox.critical(self.login_view, "Erro de Login", "Credenciais incorretas. Tente novamente.")

        # Reabilitar o botão de login após o processo de validação
        self.login_view.btn_login.setEnabled(True)
