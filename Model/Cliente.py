# Model/Cliente.py

class Cliente:
    def __init__(self, nome, contacto, email, morada, criado_em=None, id=None):
        self.id = id  # Pode ser gerado automaticamente pelo banco de dados
        self.nome = nome
        self.contacto = contacto
        self.email = email
        self.morada = morada
        self.criado_em = criado_em if criado_em else "CURRENT_TIMESTAMP"  # Caso não passe data, usa o timestamp atual
    
    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, contacto={self.contacto}, email={self.email})"
