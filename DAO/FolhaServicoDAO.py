import mysql.connector
from Model.FolhaServico import FolhaServico
from config import get_db_connection
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FolhaServicoDAO:
    def __init__(self):
        pass
    
    def criar_folha_servico(self, folha_servico):
        """Cria uma nova folha de serviço na base de dados"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                    INSERT INTO folhas_servico (veiculo_id, descricao_servico, tempo_estimado, estado) 
                    VALUES (%s, %s, %s, %s)
                    """
                    values = (folha_servico.veiculo_id, folha_servico.descricao_servico, 
                              folha_servico.tempo_estimado, folha_servico.estado)
                    
                    cursor.execute(query, values)
                    conn.commit()
                    
                    folha_id = cursor.lastrowid
                    logging.info(f"Folha de serviço criada com ID {folha_id}.")
                    return folha_id
        except mysql.connector.Error as e:
            logging.error(f"Erro ao criar folha de serviço: {e}")
            return None
    
    def criar_folha_de_orcamento(self, orcamento_id):
        """Cria uma folha de serviço a partir de um orçamento aprovado"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query_orcamento = """
                    SELECT veiculo_id, descricao, valor_estimado 
                    FROM orcamentos 
                    WHERE id = %s AND estado = 'aprovado'
                    """
                    cursor.execute(query_orcamento, (orcamento_id,))
                    orcamento_data = cursor.fetchone()
                    
                    if not orcamento_data:
                        logging.warning(f"Orçamento com ID {orcamento_id} não encontrado ou não aprovado.")
                        return None
                    
                    veiculo_id, descricao, valor_estimado = orcamento_data
                    
                    # Criar a folha de serviço
                    query_folha = """
                    INSERT INTO folhas_servico (veiculo_id, descricao_servico, estado, tempo_estimado) 
                    VALUES (%s, %s, 'pendente', %s)
                    """
                    tempo_estimado = int(valor_estimado) if valor_estimado else 60
                    cursor.execute(query_folha, (veiculo_id, descricao, tempo_estimado))
                    conn.commit()
                    
                    folha_id = cursor.lastrowid
                    logging.info(f"Folha de serviço criada a partir do orçamento com ID {orcamento_id}.")
                    return folha_id
        except mysql.connector.Error as e:
            logging.error(f"Erro ao criar folha de serviço a partir do orçamento {orcamento_id}: {e}")
            return None

    def obter_folha_por_id(self, folha_id):
        """Obtém uma folha de serviço pelo ID com informações do cliente e veículo"""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT 
                        fs.*, 
                        v.marca, 
                        v.modelo, 
                        v.matricula, 
                        c.nome AS cliente_nome 
                    FROM folhas_servico fs 
                    JOIN veiculos v ON fs.veiculo_id = v.id
                    JOIN clientes c ON v.cliente_id = c.id
                    WHERE fs.id = %s
                    """
                    cursor.execute(query, (folha_id,))
                    folha_data = cursor.fetchone()
                    
                    if folha_data:
                        logging.info(f"Folha de serviço com ID {folha_id} obtida com sucesso.")
                    else:
                        logging.warning(f"Folha de serviço com ID {folha_id} não encontrada.")
                    
                    return folha_data
        except mysql.connector.Error as e:
            logging.error(f"Erro ao obter folha de serviço com ID {folha_id}: {e}")
            return None

    def atualizar_folha_servico(self, folha_servico):
        """Atualiza os dados de uma folha de serviço existente"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                    UPDATE folhas_servico
                    SET descricao_servico = %s,
                        tempo_estimado = %s,
                        estado = %s,
                        data_inicio = %s,
                        data_conclusao = %s
                    WHERE id = %s
                    """
                    values = (
                        folha_servico.descricao_servico,
                        folha_servico.tempo_estimado,
                        folha_servico.estado,
                        folha_servico.data_inicio,
                        folha_servico.data_conclusao,
                        folha_servico.id
                    )
                    
                    cursor.execute(query, values)
                    conn.commit()
                    
                    rows_affected = cursor.rowcount
                    if rows_affected > 0:
                        logging.info(f"Folha de serviço com ID {folha_servico.id} atualizada com sucesso.")
                    else:
                        logging.warning(f"Folha de serviço com ID {folha_servico.id} não foi atualizada.")
                    
                    return rows_affected > 0
        except mysql.connector.Error as e:
            logging.error(f"Erro ao atualizar folha de serviço com ID {folha_servico.id}: {e}")
            return False

    def excluir_folha_servico(self, folha_id):
        """Exclui uma folha de serviço da base de dados"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = "DELETE FROM folhas_servico WHERE id = %s"
                    
                    cursor.execute(query, (folha_id,))
                    conn.commit()
                    
                    rows_affected = cursor.rowcount
                    if rows_affected > 0:
                        logging.info(f"Folha de serviço com ID {folha_id} excluída com sucesso.")
                    else:
                        logging.warning(f"Folha de serviço com ID {folha_id} não encontrada.")
                    
                    return rows_affected > 0
        except mysql.connector.Error as e:
            logging.error(f"Erro ao excluir folha de serviço com ID {folha_id}: {e}")
            return False

    def obter_todas_folhas_servico(self):
        """Obtém todas as folhas de serviço com informações do cliente e veículo"""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = """
                    SELECT 
                        fs.*, 
                        v.marca, 
                        v.modelo, 
                        v.matricula, 
                        c.nome AS cliente_nome 
                    FROM folhas_servico fs 
                    JOIN veiculos v ON fs.veiculo_id = v.id
                    JOIN clientes c ON v.cliente_id = c.id
                    ORDER BY fs.data_criacao DESC
                    """
                    cursor.execute(query)
                    folhas_data = cursor.fetchall()
                    
                    logging.info(f"{len(folhas_data)} folhas de serviço obtidas com sucesso.")
                    return folhas_data
        except mysql.connector.Error as e:
            logging.error(f"Erro ao obter todas as folhas de serviço: {e}")
            return []
