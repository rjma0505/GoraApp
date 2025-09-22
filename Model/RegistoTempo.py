# Model/RegistoTempo.py

class RegistoTempo:
    def __init__(self, id=None, folha_servico_id=None, utilizador_id=None,
                 inicio=None, fim=None):
        self.id = id
        self.folha_servico_id = folha_servico_id
        self.utilizador_id = utilizador_id
        self.inicio = inicio
        self.fim = fim

    def __repr__(self):
        return f"RegistoTempo(id={self.id}, folha={self.folha_servico_id}, utilizador={self.utilizador_id})"
