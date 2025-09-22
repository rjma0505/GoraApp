# Controller/OrcamentoController.py

from DAO.OrcamentoDAO import OrcamentoDAO
from DAO.FolhaServicoDAO import FolhaServicoDAO
from Model.Orcamento import Orcamento
from View.OrcamentoView import OrcamentoView
from View.CriarOrcamentoDialog import CriarOrcamentoDialog  # Import correto


class OrcamentoController:
    def __init__(self):
        self.orcamento_dao = OrcamentoDAO()      # Instância da DAO de orçamentos
        self.folha_servico_dao = FolhaServicoDAO()  # Instância da DAO de folhas de serviço

    def iniciar(self):
        """Inicia a exibição dos orçamentos"""
        orcamentos = self.orcamento_dao.listar_orcamentos_por_estado()  # Obtém os orçamentos
        self.exibir_orcamentos(orcamentos)

    def exibir_orcamentos(self, orcamentos):
        """Exibe os orçamentos na interface"""
        orcamento_view = OrcamentoView(orcamentos, self)  # Passa o controlador para a view
        orcamento_view.show()  # Exibe a janela

    def criar_orcamento(self, cliente_id, veiculo_id, descricao, valor_estimado, validade, estado="pendente"):
        """Cria um novo orçamento e salva no banco de dados"""
        orcamento = Orcamento(cliente_id, veiculo_id, descricao, valor_estimado, validade, estado)
        orcamento_id = self.orcamento_dao.criar_orcamento(orcamento)

        if orcamento_id:
            print(f"Orçamento criado com sucesso! ID: {orcamento_id}")
            self.iniciar()  # Recarrega os orçamentos
        else:
            print("Erro ao criar orçamento.")

    def atualizar_estado(self, orcamento_id, novo_estado):
        """Atualiza o estado de um orçamento"""
        atualizado = self.orcamento_dao.atualizar_estado(orcamento_id, novo_estado)
        if atualizado:
            print(f"Orçamento {orcamento_id} atualizado para estado: {novo_estado}")

            # Se o orçamento for aprovado → criar folha de serviço automaticamente
            if novo_estado == "aprovado":
                folha_id = self.folha_servico_dao.criar_folha_de_orcamento(orcamento_id)
                if folha_id:
                    print(f"Folha de serviço criada automaticamente! ID: {folha_id}")
                else:
                    print("Erro ao criar folha de serviço a partir do orçamento aprovado.")

            self.iniciar()  # Recarregar orçamentos na interface
        else:
            print(f"Erro ao atualizar estado do orçamento {orcamento_id}")
