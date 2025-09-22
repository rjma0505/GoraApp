class FolhaServico:
    def __init__(self, id=None, orcamento_id=None, veiculo_id=None, descricao_servico=None, estado="pendente",
                 tempo_real=0, data_criacao=None, data_conclusao=None):
        self.id = id
        self.orcamento_id = orcamento_id
        self.veiculo_id = veiculo_id
        self.descricao_servico = descricao_servico
        self.estado = estado
        self.tempo_real = tempo_real
        self.data_criacao = data_criacao
        self.data_conclusao = data_conclusao

    def __repr__(self):
        return f"FolhaServico(id={self.id}, estado={self.estado})"
