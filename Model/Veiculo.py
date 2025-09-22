# Model/Veiculo.py
import re
from typing import Optional

class Veiculo:
    def __init__(self, id: Optional[int] = None, cliente_id: Optional[int] = None,
                 marca: Optional[str] = None, modelo: Optional[str] = None,
                 matricula: Optional[str] = None, pais: Optional[str] = None):
        self.id = id
        self.cliente_id = cliente_id
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula
        self.pais = pais
        
        # Validação da matrícula e país
        if matricula and not self.validar_matricula(matricula):
            raise ValueError("Matrícula inválida.")
        
        if pais and not self.validar_pais(pais):
            raise ValueError("País inválido.")

    def __repr__(self) -> str:
        """
        Retorna uma representação detalhada do objeto veiculo.
        """
        return (f"Veiculo(id={self.id}, cliente_id={self.cliente_id}, "
                f"marca='{self.marca}', modelo='{self.modelo}', "
                f"matricula='{self.matricula}', pais='{self.pais}')")
    
    def to_dict(self) -> dict:
        """
        Retorna o veiculo como um dicionário (útil para APIs ou exportação de dados).
        """
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "marca": self.marca,
            "modelo": self.modelo,
            "matricula": self.matricula,
            "pais": self.pais
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Veiculo':
        """
        Constrói um objeto Veiculo a partir de um dicionário de dados.
        """
        return cls(
            id=data.get('id'),
            cliente_id=data.get('cliente_id'),
            marca=data.get('marca'),
            modelo=data.get('modelo'),
            matricula=data.get('matricula'),
            pais=data.get('pais')
        )
    
    def validar_matricula(self, matricula: str) -> bool:
        """
        Valida o formato da matrícula (exemplo: Portugal: XX-XX-XX ou XX-XX-XX).
        Pode ser ajustado para outros países.
        """
        # Exemplo de padrão para matrículas portuguesas (ajuste conforme necessário)
        pattern = r"^[A-Z]{2}-\d{2}-[A-Z]{2}$"
        return bool(re.match(pattern, matricula))

    def validar_pais(self, pais: str) -> bool:
        """
        Valida se o país é uma string válida. Pode-se expandir para uma lista de países válidos.
        """
        # Lista simplificada de países (pode ser expandida)
        paises_validos = ["Portugal", "Brasil", "Espanha", "França", "Alemanha"]
        return pais in paises_validos
