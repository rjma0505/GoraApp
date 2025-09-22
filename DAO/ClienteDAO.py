# DAO/ClienteDAO.py

import mysql.connector
from Model.Cliente import Cliente
from config import get_db_connection

class ClienteDAO:
    def __init__(self):
        pass
    
    def adicionar_cliente(self, cliente):
        """Adiciona um novo cliente no banco de dados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO clientes (nome, contacto, email, morada, criado_em) 
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (cliente.nome, cliente.contacto, cliente.email, cliente.morada, cliente.criado_em)
            
            cursor.execute(query, values)
            conn.commit()
            
            cliente.id = cursor.lastrowid  # Captura o ID gerado automaticamente
            cursor.close()
            conn.close()
            
            print(f"Cliente {cliente.nome} adicionado com sucesso!")
        
        except mysql.connector.Error as e:
            print(f"Erro ao adicionar cliente: {e}")
