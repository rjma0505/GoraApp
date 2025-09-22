import mysql.connector
from config import get_db_connection

class FolhaServicoDAO:
    def __init__(self):
        pass

    def criar_folha_servico(self, dados):
        """Cria uma nova folha de serviço no banco de dados."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO folhas_servico (orcamento_id, veiculo_id, descricao_servico, estado, tempo_real)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                dados['orcamento_id'],
                dados['veiculo_id'],
                dados['descricao_servico'],
                dados.get('estado', 'pendente'),
                dados.get('tempo_real', 0)
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao criar folha de serviço: {e}")
            return False

    def obter_todas_folhas_servico(self):
        """Retorna todas as folhas de serviço do banco de dados."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM folhas_servico")
            folhas = cursor.fetchall()
            cursor.close()
            conn.close()
            return folhas
        except mysql.connector.Error as e:
            print(f"Erro ao obter folhas de serviço: {e}")
            return []

    def obter_folha_por_id(self, folha_id):
        """Retorna uma folha de serviço específica pelo ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM folhas_servico WHERE id = %s", (folha_id,))
            folha = cursor.fetchone()
            cursor.close()
            conn.close()
            return folha
        except mysql.connector.Error as e:
            print(f"Erro ao obter folha: {e}")
            return None

    def atualizar_folha_servico(self, folha: dict):
        """Atualiza os dados de uma folha de serviço existente."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            UPDATE folhas_servico
            SET descricao_servico=%s, estado=%s, tempo_real=%s
            WHERE id=%s
            """
            cursor.execute(query, (
                folha['descricao_servico'],
                folha['estado'],
                folha['tempo_real'],
                folha['id']
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar folha: {e}")
            return False

    def excluir_folha_servico(self, folha_id):
        """Exclui uma folha de serviço pelo ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM folhas_servico WHERE id=%s", (folha_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao excluir folha: {e}")
            return False

    def obter_folhas_aprovadas(self):
        """
        Retorna apenas folhas de serviços associadas a orçamentos aprovados,
        incluindo informações de cliente e veículo.
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT fs.id, fs.orcamento_id, fs.veiculo_id, fs.descricao_servico, fs.estado, fs.tempo_real,
                   c.nome AS cliente_nome, v.marca AS veiculo_marca, v.modelo AS veiculo_modelo
            FROM folhas_servico fs
            JOIN orcamentos o ON fs.orcamento_id = o.id
            JOIN clientes c ON o.cliente_id = c.id
            JOIN veiculos v ON o.veiculo_id = v.id
            WHERE o.estado = 'aprovado'
            ORDER BY fs.id DESC
            """
            cursor.execute(query)
            folhas = cursor.fetchall()
            cursor.close()
            conn.close()
            return folhas
        except mysql.connector.Error as e:
            print(f"Erro ao obter folhas aprovadas: {e}")
            return []
