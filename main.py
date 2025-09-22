import sys
from PyQt5.QtWidgets import QApplication
from Controller.LoginController import LoginController  # Corrigido para a importação correta
from config import get_db_connection  # A importação do banco de dados

def main():
    app = QApplication(sys.argv)
    
    # Verifica a conexão com o banco de dados
    try:
        conn = get_db_connection()  # Certificado para 'get_db_connection'
        if conn and conn.is_connected():
            print("Conexão com a base de dados bem-sucedida!")
            conn.close()  # Fecha a conexão de teste
        else:
            print("Erro: A conexão com a base de dados falhou.")
            return 1
    except Exception as e:
        print(f"Erro ao conectar com a base de dados: {e}")
        return 1

    # Inicia o controlador de login
    login_controller = LoginController()
    login_controller.iniciar()  # Chamando o início do login

    sys.exit(app.exec_())  # Garante que o aplicativo execute corretamente no loop de eventos

if __name__ == "__main__":
    main()