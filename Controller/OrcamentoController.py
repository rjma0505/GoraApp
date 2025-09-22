# Controller/OrcamentoController.py

from DAO.OrcamentoDAO import OrcamentoDAO
from Model.Orcamento import Orcamento
from View.OrcamentoView import OrcamentoView
from View.CriarOrcamentoDialog import CriarOrcamentoDialog  # Certifique-se de importar corretamente

class OrcamentoController:
    def __init__(self):
        self.orcamento_dao = OrcamentoDAO()  # Instância da DAO de orçamentos

    def iniciar(self):
        """Inicia a exibição dos orçamentos"""
        orcamentos = self.orcamento_dao.listar_orcamentos_por_estado()  # Obtém os orçamentos
        self.exibir_orcamentos(orcamentos)

    def exibir_orcamentos(self, orcamentos):
        """Exibe os orçamentos na interface"""
        if orcamentos:
            orcamento_view = OrcamentoView(orcamentos, self)  # Passa o controlador para a view
            orcamento_view.show()  # Exibe a janela
        else:
            print("Nenhum orçamento encontrado.")
            orcamento_view = OrcamentoView(orcamentos, self)  # Passa o controlador para a view
            orcamento_view.show()

    def criar_orcamento(self, cliente_id, veiculo_id, descricao, valor_estimado, validade, estado):
        """Cria um novo orçamento e salva no banco de dados"""
        orcamento = Orcamento(cliente_id, veiculo_id, descricao, valor_estimado, validade, estado)
        orcamento_id = self.orcamento_dao.criar_orcamento(orcamento)
        
        if orcamento_id:
            print(f"Orçamento criado com sucesso! ID: {orcamento_id}")
            self.iniciar()  # Recarrega os orçamentos
        else:
            print("Erro ao criar orçamento.")
