import mysql.connector
import bcrypt
import logging

# --- Função de segurança para gerar hash bcrypt ---
def encriptar_password(senha: str) -> str:
    """Gera o hash de uma senha utilizando bcrypt."""
    hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    return hash_senha.decode('utf-8')

# --- Função para conectar ao MySQL ---
def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234ra",
            database="goraapp_db"
        )
    except mysql.connector.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        raise  # Lança o erro novamente para o chamador

# --- Função para criar ou atualizar utilizador ---
def criar_ou_atualizar_utilizador(username: str, nome: str, senha: str, role: str):
    """Cria ou atualiza um utilizador no banco de dados."""
    try:
        conn = get_db_connection()  # Chama a função corrigida get_db_connection()
        with conn.cursor() as cursor:
            # Gerar o hash da senha
            hash_pass = encriptar_password(senha)
            
            # Verificar se o utilizador já existe
            cursor.execute("SELECT id FROM utilizadores WHERE username=%s", (username,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Atualizar utilizador existente
                cursor.execute(
                    "UPDATE utilizadores SET password_hash=%s, role=%s, nome=%s WHERE username=%s",
                    (hash_pass, role, nome, username)
                )
                logging.info(f"Utilizador '{username}' atualizado com nova senha e role '{role}'.")
            else:
                # Inserir novo utilizador
                cursor.execute(
                    "INSERT INTO utilizadores (nome, username, password_hash, role) VALUES (%s, %s, %s, %s)",
                    (nome, username, hash_pass, role)
                )
                logging.info(f"Novo utilizador '{username}' criado com role '{role}'.")
            
            # Commit das mudanças
            conn.commit()
    
    except mysql.connector.Error as e:
        logging.error(f"Erro ao criar ou atualizar utilizador: {e}")
        conn.rollback()  # Desfaz a operação em caso de erro
    finally:
        conn.close()  # Sempre fecha a conexão após terminar

# --- Exemplos de uso ---
if __name__ == "__main__":
    # Atualizar a password do admin
    criar_ou_atualizar_utilizador("admin", "Administrador", "admin123", "admin")
    
    # Criar um funcionário
    criar_ou_atualizar_utilizador("funcionario01", "Funcionário 01", "func123", "funcionario")
