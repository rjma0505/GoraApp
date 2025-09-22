# DAO/VeiculoDAO.py
import mysql.connector
from Model.Veiculo import Veiculo
from config import get_db_connection

class VeiculoDAO:
    def __init__(self):
        pass

    def criar_veiculo(self, veiculo: Veiculo):
        """Cria um novo veículo na base de dados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO veiculos (cliente_id, marca, modelo, matricula, pais) 
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (veiculo.cliente_id, veiculo.marca, veiculo.modelo, veiculo.matricula, veiculo.pais)
            cursor.execute(query, values)
            conn.commit()
            veiculo_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return veiculo_id
        except mysql.connector.Error as e:
            print(f"Erro ao criar veículo: {e}")
            return None

    def obter_veiculo_por_id(self, veiculo_id: int):
        """Obtém um veículo pelo ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            SELECT v.*, c.nome as cliente_nome 
            FROM veiculos v 
            JOIN clientes c ON v.cliente_id = c.id 
            WHERE v.id = %s
            """
            cursor.execute(query, (veiculo_id,))
            resultado = cursor.fetchone()
            if resultado:
                veiculo = Veiculo(
                    id=resultado[0],
                    cliente_id=resultado[1],
                    marca=resultado[2],
                    modelo=resultado[3],
                    matricula=resultado[4],
                    pais=resultado[5],
                    validar=False  # <-- importante
                )
                veiculo.cliente_nome = resultado[6]
                cursor.close()
                conn.close()
                return veiculo
            cursor.close()
            conn.close()
            return None
        except mysql.connector.Error as e:
            print(f"Erro ao obter veículo: {e}")
            return None

    def listar_veiculos_por_cliente(self, cliente_id: int):
        """Lista todos os veículos de um cliente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM veiculos WHERE cliente_id = %s ORDER BY marca, modelo"
            cursor.execute(query, (cliente_id,))
            resultados = cursor.fetchall()
            veiculos = []
            for resultado in resultados:
                veiculo = Veiculo(
                    id=resultado[0],
                    cliente_id=resultado[1],
                    marca=resultado[2],
                    modelo=resultado[3],
                    matricula=resultado[4],
                    pais=resultado[5],
                    validar=False  # <-- desativa validação
                )
                veiculos.append(veiculo)
            cursor.close()
            conn.close()
            return veiculos
        except mysql.connector.Error as e:
            print(f"Erro ao listar veículos: {e}")
            return []

    def listar_todos_veiculos(self):
        """Lista todos os veículos com informações do cliente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            SELECT v.*, c.nome as cliente_nome 
            FROM veiculos v 
            JOIN clientes c ON v.cliente_id = c.id 
            ORDER BY c.nome, v.marca, v.modelo
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            veiculos = []
            for resultado in resultados:
                veiculo = Veiculo(
                    id=resultado[0],
                    cliente_id=resultado[1],
                    marca=resultado[2],
                    modelo=resultado[3],
                    matricula=resultado[4],
                    pais=resultado[5],
                    validar=False  # <-- desativa validação
                )
                veiculo.cliente_nome = resultado[6]
                veiculos.append(veiculo)
            cursor.close()
            conn.close()
            return veiculos
        except mysql.connector.Error as e:
            print(f"Erro ao listar veículos: {e}")
            return []

    def atualizar_veiculo(self, veiculo: Veiculo):
        """Atualiza um veículo existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            UPDATE veiculos 
            SET cliente_id = %s, marca = %s, modelo = %s, matricula = %s, pais = %s 
            WHERE id = %s
            """
            values = (veiculo.cliente_id, veiculo.marca, veiculo.modelo, veiculo.matricula, veiculo.pais, veiculo.id)
            cursor.execute(query, values)
            conn.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conn.close()
            return linhas_afetadas > 0
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar veículo: {e}")
            return False

    def eliminar_veiculo(self, veiculo_id: int):
        """Elimina um veículo"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM veiculos WHERE id = %s"
            cursor.execute(query, (veiculo_id,))
            conn.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conn.close()
            return linhas_afetadas > 0
        except mysql.connector.Error as e:
            print(f"Erro ao eliminar veículo: {e}")
            return False

    def verificar_matricula_existe(self, matricula: str, veiculo_id: int = None):
        """Verifica se uma matrícula já existe"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if veiculo_id:
                query = "SELECT COUNT(*) FROM veiculos WHERE matricula = %s AND id != %s"
                cursor.execute(query, (matricula, veiculo_id))
            else:
                query = "SELECT COUNT(*) FROM veiculos WHERE matricula = %s"
                cursor.execute(query, (matricula,))
            resultado = cursor.fetchone()
            existe = resultado[0] > 0
            cursor.close()
            conn.close()
            return existe
        except mysql.connector.Error as e:
            print(f"Erro ao verificar matrícula: {e}")
            return False

    def pesquisar_veiculos(self, termo_pesquisa: str):
        """Pesquisa veículos por marca, modelo ou matrícula"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            SELECT v.*, c.nome as cliente_nome 
            FROM veiculos v 
            JOIN clientes c ON v.cliente_id = c.id 
            WHERE v.marca LIKE %s OR v.modelo LIKE %s OR v.matricula LIKE %s
            ORDER BY c.nome, v.marca, v.modelo
            """
            termo = f"%{termo_pesquisa}%"
            cursor.execute(query, (termo, termo, termo))
            resultados = cursor.fetchall()
            veiculos = []
            for resultado in resultados:
                veiculo = Veiculo(
                    id=resultado[0],
                    cliente_id=resultado[1],
                    marca=resultado[2],
                    modelo=resultado[3],
                    matricula=resultado[4],
                    pais=resultado[5],
                    validar=False  # <-- desativa validação
                )
                veiculo.cliente_nome = resultado[6]
                veiculos.append(veiculo)
            cursor.close()
            conn.close()
            return veiculos
        except mysql.connector.Error as e:
            print(f"Erro ao pesquisar veículos: {e}")
            return []
