# Model/FolhaServico.py

class FolhaServico:
    def __init__(self, id=None, veiculo_id=None, descricao_servico=None, estado="pendente",
                 data_criacao=None, data_conclusao=None, tempo_estimado=None, tempo_real=None):
        self.id = id
        self.veiculo_id = veiculo_id
        self.descricao_servico = descricao_servico
        self.estado = estado
        self.data_criacao = data_criacao
        self.data_conclusao = data_conclusao
        self.tempo_estimado = tempo_estimado
        self.tempo_real = tempo_real

    def __repr__(self):
        return f"FolhaServico(id={self.id}, estado={self.estado})"
