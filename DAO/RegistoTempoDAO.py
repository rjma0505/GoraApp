import mysql.connector
from datetime import datetime
from config import get_db_connection  # Corrigido para o nome correto


class RegistoTempoDAO:
    def __init__(self):
        pass

    def iniciar_registo_tempo(self, folha_servico_id, utilizador_id):
        """Inicia um novo registo de tempo para uma folha de serviço."""
        try:
            conn = get_db_connection()  # Corrigido para get_db_connection
            cursor = conn.cursor()
            
            # 1. Verificar se já existe um registo ativo para esta folha de serviço
            query_check = """
            SELECT id FROM registos_tempo 
            WHERE folha_servico_id = %s AND fim IS NULL
            """
            cursor.execute(query_check, (folha_servico_id,))
            if cursor.fetchone():
                print("Já existe um registo de tempo ativo para esta folha de serviço.")
                cursor.close()
                conn.close()
                return None

            # 2. Inserir um novo registo com a hora de início
            query_insert = """
            INSERT INTO registos_tempo (folha_servico_id, utilizador_id, inicio)
            VALUES (%s, %s, NOW())
            """
            cursor.execute(query_insert, (folha_servico_id, utilizador_id))
            
            # 3. Atualizar o estado da folha de serviço para 'em_progresso'
            query_update_fs = """
            UPDATE folhas_servico
            SET estado = 'em_progresso', data_inicio = NOW()
            WHERE id = %s AND estado = 'pendente'
            """
            cursor.execute(query_update_fs, (folha_servico_id,))

            conn.commit()
            
            registo_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return registo_id
            
        except mysql.connector.Error as e:
            print(f"Erro ao iniciar registo de tempo: {e}")
            return None

    def finalizar_registo_tempo(self, folha_servico_id):
        """Finaliza um registo de tempo ativo para uma folha de serviço."""
        try:
            conn = get_db_connection()  # Corrigido para get_db_connection
            cursor = conn.cursor()
            
            # 1. Encontrar o registo ativo
            query_select = """
            SELECT id, inicio FROM registos_tempo 
            WHERE folha_servico_id = %s AND fim IS NULL
            """
            cursor.execute(query_select, (folha_servico_id,))
            registo_data = cursor.fetchone()
            
            if not registo_data:
                print("Nenhum registo de tempo ativo encontrado para esta folha de serviço.")
                cursor.close()
                conn.close()
                return False
                
            registo_id, inicio_str = registo_data
            inicio = datetime.fromtimestamp(inicio_str.timestamp())

            # 2. Atualizar o registo com a hora de fim
            query_update = """
            UPDATE registos_tempo
            SET fim = NOW()
            WHERE id = %s
            """
            cursor.execute(query_update, (registo_id,))

            # 3. Calcular o tempo decorrido e atualizar a folha de serviço
            agora = datetime.now()
            tempo_decorrido_minutos = int((agora - inicio).total_seconds() / 60)
            
            query_update_fs = """
            UPDATE folhas_servico
            SET tempo_real = IFNULL(tempo_real, 0) + %s
            WHERE id = %s
            """
            cursor.execute(query_update_fs, (tempo_decorrido_minutos, folha_servico_id))

            conn.commit()
            cursor.close()
            conn.close()
            
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao finalizar registo de tempo: {e}")
            return False
            
    def obter_registos_por_folha(self, folha_servico_id):
        """Obtém todos os registos de tempo para uma folha de serviço."""
        try:
            conn = get_db_connection()  # Corrigido para get_db_connection
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT 
                rt.id, 
                rt.inicio, 
                rt.fim, 
                rt.folha_servico_id,
                u.nome AS utilizador_nome
            FROM registos_tempo rt
            JOIN utilizadores u ON rt.utilizador_id = u.id
            WHERE rt.folha_servico_id = %s
            ORDER BY rt.inicio
            """
            
            cursor.execute(query, (folha_servico_id,))
            registos = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return registos
            
        except mysql.connector.Error as e:
            print(f"Erro ao obter registos de tempo: {e}")
            return []
