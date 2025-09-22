# Model/Orcamento.py

class Orcamento:
    def __init__(self, cliente_id, veiculo_id, descricao, valor_estimado, validade, estado, id=None, data_criacao=None):
        self.id = id  # A ID pode ser gerada automaticamente no banco de dados
        self.cliente_id = cliente_id
        self.veiculo_id = veiculo_id
        self.descricao = descricao
        self.valor_estimado = valor_estimado
        self.validade = validade
        self.estado = estado
        self.data_criacao = data_criacao if data_criacao else "CURRENT_TIMESTAMP"  # Default para o timestamp atual se não fornecido

    def __repr__(self):
        return f"Orcamento(id={self.id}, cliente_id={self.cliente_id}, veiculo_id={self.veiculo_id}, descricao={self.descricao}, valor_estimado={self.valor_estimado}, estado={self.estado})"
