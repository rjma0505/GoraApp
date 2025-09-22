import re

REGEX_MATRICULAS = {
    "PT": [
        r"^[A-Z]{2}-\d{2}-[A-Z]{2}$",
        r"^\d{2}-[A-Z]{2}-\d{2}$",
        r"^[A-Z]{2}-\d{2}-\d{2}$",
        r"^\d{2}-\d{2}-[A-Z]{2}$"
    ],
    "ES": [r"^\d{4}-[A-Z]{3}$", r"^[A-Z]{1,2}-\d{4}-[A-Z]{1,2}$"],
    "FR": [r"^[A-Z]{2}-\d{3}-[A-Z]{2}$"],
    "LU": [r"^[A-Z]{2}-\d{4}$", r"^\d{3,5}$"],
    "CH": [r"^[A-Z]{2}-\d{1,6}$"]
}

def validar_matricula(matricula: str, pais: str) -> bool:
    matricula = matricula.strip().upper()
    regras = REGEX_MATRICULAS.get(pais, [])
    return any(re.match(r, matricula) for r in regras)
