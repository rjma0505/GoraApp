import mysql.connector
import bcrypt
import logging
from config import get_db_connection
from typing import Optional, List
from Model.Utilizador import Utilizador  # Certifique-se de que o caminho esteja correto

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UtilizadorDAO:
    """
    Classe de Acesso a Dados para a gestão de Utilizadores.
    Lida com todas as operações de base de dados para a tabela 'utilizadores'.
    """
    def __init__(self):
        pass

    def criar_utilizador(self, nome: str, username: str, password: str, role: str) -> Optional[int]:
        """Cria um novo utilizador na base de dados."""
        try:
            if self.username_existe(username):
                logging.warning(f"O nome de utilizador '{username}' já existe.")
                return None  # Ou lançar exceção se preferir

            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Hash da palavra-passe com bcrypt
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Não precisa do .decode('utf-8')

                    query = "INSERT INTO utilizadores (nome, username, password_hash, role) VALUES (%s, %s, %s, %s)"
                    values = (nome, username, hashed_password, role)
                    cursor.execute(query, values)
                    conn.commit()

                    utilizador_id = cursor.lastrowid
                    logging.info(f"Novo utilizador criado com ID: {utilizador_id}")
                    return utilizador_id

        except mysql.connector.Error as e:
            logging.error(f"Erro ao criar utilizador: {e}")
            return None

    def username_existe(self, username: str) -> bool:
        """Verifica se o nome de utilizador já existe na base de dados."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = "SELECT 1 FROM utilizadores WHERE username = %s LIMIT 1"
                    cursor.execute(query, (username,))
                    return cursor.fetchone() is not None
        except mysql.connector.Error as e:
            logging.error(f"Erro ao verificar nome de utilizador: {e}")
            return False

    def obter_utilizador(self, username: str) -> Optional[Utilizador]:
        """Obtém um utilizador pelo nome de utilizador."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = "SELECT * FROM utilizadores WHERE username = %s"
                    cursor.execute(query, (username,))
                    utilizador_data = cursor.fetchone()

            if utilizador_data:
                return Utilizador(**utilizador_data)
            return None

        except mysql.connector.Error as e:
            logging.error(f"Erro ao obter utilizador: {e}")
            return None

    def obter_utilizador_por_id(self, utilizador_id: int) -> Optional[Utilizador]:
        """Obtém um utilizador pelo ID."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = "SELECT * FROM utilizadores WHERE id = %s"
                    cursor.execute(query, (utilizador_id,))
                    utilizador_data = cursor.fetchone()

            if utilizador_data:
                return Utilizador(**utilizador_data)
            return None

        except mysql.connector.Error as e:
            logging.error(f"Erro ao obter utilizador por ID: {e}")
            return None

    def obter_todos_utilizadores(self) -> List[Utilizador]:
        """Obtém uma lista de todos os utilizadores."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = "SELECT * FROM utilizadores ORDER BY username"
                    cursor.execute(query)
                    utilizadores_data = cursor.fetchall()

            return [Utilizador(**data) for data in utilizadores_data]

        except mysql.connector.Error as e:
            logging.error(f"Erro ao obter todos os utilizadores: {e}")
            return []

    def atualizar_password(self, utilizador_id: int, nova_password: str) -> bool:
        """Atualiza a palavra-passe de um utilizador."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Novo hash da palavra-passe
                    hashed_password = bcrypt.hashpw(nova_password.encode('utf-8'), bcrypt.gensalt())  # Não precisa do .decode('utf-8')

                    query = "UPDATE utilizadores SET password_hash = %s WHERE id = %s"
                    cursor.execute(query, (hashed_password, utilizador_id))
                    conn.commit()

                    rows_affected = cursor.rowcount
                    logging.info(f"Password atualizada para o utilizador ID: {utilizador_id}")
                    return rows_affected > 0

        except mysql.connector.Error as e:
            logging.error(f"Erro ao atualizar palavra-passe: {e}")
            return False

    def excluir_utilizador(self, utilizador_id: int) -> bool:
        """Exclui um utilizador da base de dados.""" 
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = "DELETE FROM utilizadores WHERE id = %s"
                    cursor.execute(query, (utilizador_id,))
                    conn.commit()

                    rows_affected = cursor.rowcount
                    if rows_affected > 0:
                        logging.info(f"Utilizador ID: {utilizador_id} excluído com sucesso.")
                    else:
                        logging.warning(f"Não foi possível excluir o utilizador ID: {utilizador_id}")
                    return rows_affected > 0

        except mysql.connector.Error as e:
            logging.error(f"Erro ao excluir utilizador: {e}")
            return False

    def verificar_password(self, utilizador_id: int, password: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        utilizador = self.obter_utilizador_por_id(utilizador_id)
        if utilizador:
            return bcrypt.checkpw(password.encode('utf-8'), utilizador.password_hash.encode('utf-8'))
        return False
