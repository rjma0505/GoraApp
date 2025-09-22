import mysql.connector
from Model.Cliente import Cliente
from config import get_db_connection

class ClienteDAO:
    def __init__(self):
        pass
    
    def adicionar_cliente(self, cliente: Cliente):
        """Adiciona um novo cliente no banco de dados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO clientes (nome, contacto, email, morada) 
            VALUES (%s, %s, %s, %s)
            """
            values = (cliente.nome, cliente.contacto, cliente.email, cliente.morada)
            
            cursor.execute(query, values)
            conn.commit()
            
            cliente.id = cursor.lastrowid
            cursor.close()
            conn.close()
        
        except mysql.connector.Error as e:
            print(f"Erro ao adicionar cliente: {e}")

    def listar_clientes(self):
        """Retorna a lista de clientes"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nome, contacto, email, morada FROM clientes ORDER BY nome")
            clientes = cursor.fetchall()
            cursor.close()
            conn.close()
            return clientes
        except mysql.connector.Error as e:
            print(f"Erro ao listar clientes: {e}")
            return []

    def obter_cliente_por_id(self, cliente_id: int) -> Cliente:
        """Retorna um cliente específico pelo ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                return Cliente(
                    id=row["id"],
                    nome=row["nome"],
                    contacto=row.get("contacto"),
                    email=row.get("email"),
                    morada=row.get("morada")
                )
            return None
        except mysql.connector.Error as e:
            print(f"Erro ao obter cliente: {e}")
            return None

    def atualizar_cliente(self, cliente: Cliente):
        """Atualiza os dados de um cliente existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            UPDATE clientes
            SET nome = %s, contacto = %s, email = %s, morada = %s
            WHERE id = %s
            """
            values = (cliente.nome, cliente.contacto, cliente.email, cliente.morada, cliente.id)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar cliente: {e}")

    def remover_cliente(self, cliente_id: int):
        """Remove um cliente pelo ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(f"Erro ao remover cliente: {e}")
