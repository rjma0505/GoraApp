# Model/Veiculo.py
import re
from typing import Optional

class Veiculo:
    PADROES_MATRICULA = {
        "Portugal": [
            r"^\d{2}-\d{2}-\d{2}$",
            r"^[A-Z]{2}-\d{2}-[A-Z]{2}$",
            r"^\d{2}-[A-Z]{2}-\d{2}$",
            r"^[A-Z]{2}-\d{2}-\d{2}$",
            r"^\d{2}-\d{2}-[A-Z]{2}$",
            r"^\d{2}-[A-Z]{2}-[A-Z]{2}$",
        ],
        "Espanha": [
            r"^\d{4} [A-Z]{3}$",
            r"^[A-Z]{1,2}-\d{1,4}-[A-Z]{1,2}$",
        ],
        "França": [
            r"^\d{2}-[A-Z]{2}-\d{3}$",
            r"^\d{2}[A-Z]{2}\d{3}$",
        ],
        "Alemanha": [
            r"^[A-Z]{1,3}-[A-Z]{1,2} \d{1,4}$",
        ],
        "Luxemburgo": [
            r"^[A-Z]{1,2} \d{1,4}$",
        ],
        "Suíça": [
            r"^[A-Z]{2} \d{1,4}$",
        ]
    }

    def __init__(self, id: Optional[int] = None, cliente_id: Optional[int] = None,
                 marca: Optional[str] = None, modelo: Optional[str] = None,
                 matricula: Optional[str] = None, pais: Optional[str] = None,
                 validar: bool = True):
        """
        Se validar=True, faz validação da matrícula.
        Se validar=False, cria o objeto sem validar (útil para instanciar veículos antigos da DB)
        """
        self.id = id
        self.cliente_id = cliente_id
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula
        self.pais = pais

        if validar and pais and matricula:
            if not self.validar_matricula_por_pais(matricula, pais):
                raise ValueError(f"Matrícula inválida para o país {pais}.")

    def __repr__(self) -> str:
        return (f"Veiculo(id={self.id}, cliente_id={self.cliente_id}, "
                f"marca='{self.marca}', modelo='{self.modelo}', "
                f"matricula='{self.matricula}', pais='{self.pais}')")

    @classmethod
    def validar_matricula_por_pais(cls, matricula: str, pais: str) -> bool:
        padroes_pais = cls.PADROES_MATRICULA.get(pais)
        if not padroes_pais:
            return False
        for padrao in padroes_pais:
            if re.fullmatch(padrao, matricula):
                return True
        return False

    def to_dict(self) -> dict:
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
        return cls(
            id=data.get('id'),
            cliente_id=data.get('cliente_id'),
            marca=data.get('marca'),
            modelo=data.get('modelo'),
            matricula=data.get('matricula'),
            pais=data.get('pais'),
            validar=False  # aqui não validamos, para evitar erros com matrículas antigas
        )
