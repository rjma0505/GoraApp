# DAO/OrcamentoDAO.py

import mysql.connector
from Model.Orcamento import Orcamento
from config import get_db_connection

class OrcamentoDAO:
    def __init__(self):
        pass

    def criar_orcamento(self, orcamento: Orcamento):
        """Cria um novo orçamento no banco de dados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO orcamentos (cliente_id, veiculo_id, descricao, valor_estimado, validade, estado, data_criacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                orcamento.cliente_id,
                orcamento.veiculo_id,
                orcamento.descricao,
                orcamento.valor_estimado,
                orcamento.validade,
                orcamento.estado,
                orcamento.data_criacao
            )
            cursor.execute(query, values)
            conn.commit()
            orcamento.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return orcamento.id
        except mysql.connector.Error as e:
            print(f"Erro ao criar orçamento: {e}")
            return None

    def listar_todos_orcamentos(self):
        """Lista todos os orçamentos com informações de cliente e veículo"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT o.*, c.nome as cliente_nome, v.marca as veiculo_marca, v.modelo as veiculo_modelo
            FROM orcamentos o
            JOIN clientes c ON o.cliente_id = c.id
            JOIN veiculos v ON o.veiculo_id = v.id
            ORDER BY o.data_criacao DESC
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return resultados
        except mysql.connector.Error as e:
            print(f"Erro ao listar orçamentos: {e}")
            return []

    def obter_orcamento_por_id(self, orcamento_id):
        """Retorna um orçamento pelo ID, incluindo informações do cliente e veículo"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT o.*, c.nome as cliente_nome, v.marca as veiculo_marca, v.modelo as veiculo_modelo
            FROM orcamentos o
            JOIN clientes c ON o.cliente_id = c.id
            JOIN veiculos v ON o.veiculo_id = v.id
            WHERE o.id = %s
            """
            cursor.execute(query, (orcamento_id,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return resultado
        except mysql.connector.Error as e:
            print(f"Erro ao obter orçamento: {e}")
            return None

    def atualizar_orcamento(self, orcamento: Orcamento):
        """Atualiza um orçamento existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            UPDATE orcamentos
            SET cliente_id=%s, veiculo_id=%s, descricao=%s, valor_estimado=%s, validade=%s, estado=%s
            WHERE id=%s
            """
            values = (
                orcamento.cliente_id,
                orcamento.veiculo_id,
                orcamento.descricao,
                orcamento.valor_estimado,
                orcamento.validade,
                orcamento.estado,
                orcamento.id
            )
            cursor.execute(query, values)
            conn.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conn.close()
            return linhas_afetadas > 0
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar orçamento: {e}")
            return False

    def eliminar_orcamento(self, orcamento_id):
        """Elimina um orçamento pelo ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orcamentos WHERE id=%s", (orcamento_id,))
            conn.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conn.close()
            return linhas_afetadas > 0
        except mysql.connector.Error as e:
            print(f"Erro ao eliminar orçamento: {e}")
            return False
