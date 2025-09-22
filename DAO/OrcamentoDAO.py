# DAO/OrcamentoDAO.py

import mysql.connector
from Model.Orcamento import Orcamento
from config import get_db_connection

class OrcamentoDAO:
    def __init__(self):
        pass
    
    def criar_orcamento(self, orcamento):
        """Cria um novo orçamento na base de dados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO orcamentos (cliente_id, veiculo_id, descricao, valor_estimado, validade, estado) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (orcamento.cliente_id, orcamento.veiculo_id, orcamento.descricao, 
                     orcamento.valor_estimado, orcamento.validade, orcamento.estado)
            
            cursor.execute(query, values)
            conn.commit()
            
            orcamento_id = cursor.lastrowid  # Obtém o ID do último orçamento inserido
            cursor.close()
            conn.close()
            
            return orcamento_id  # Retorna o ID do orçamento criado
            
        except mysql.connector.Error as e:
            print(f"Erro ao criar orçamento: {e}")
            return None
