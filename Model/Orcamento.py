# Model/Orcamento.py

from typing import Optional
from datetime import datetime

class Orcamento:
    def __init__(self, cliente_id: int, veiculo_id: int, descricao: str,
                 valor_estimado: float, validade: str, estado: str = "pendente",
                 id: Optional[int] = None, data_criacao: Optional[str] = None):
        self.id = id
        self.cliente_id = cliente_id
        self.veiculo_id = veiculo_id
        self.descricao = descricao
        self.valor_estimado = valor_estimado
        self.validade = validade
        self.estado = estado
        self.data_criacao = data_criacao if data_criacao else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"Orcamento(id={self.id}, cliente_id={self.cliente_id}, veiculo_id={self.veiculo_id}, descricao='{self.descricao}', valor_estimado={self.valor_estimado}, estado='{self.estado}')"

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "veiculo_id": self.veiculo_id,
            "descricao": self.descricao,
            "valor_estimado": self.valor_estimado,
            "validade": self.validade,
            "estado": self.estado,
            "data_criacao": self.data_criacao
        }
