from DAO.OrcamentoDAO import OrcamentoDAO
from DAO.FolhaServicoDAO import FolhaServicoDAO
from Model.Orcamento import Orcamento
from View.OrcamentoView import OrcamentoView
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OrcamentoController:
    def __init__(self):
        self.dao = OrcamentoDAO()
        self.fs_dao = FolhaServicoDAO()
        self.view = None

    def iniciar(self):
        """Carrega todos os orçamentos e exibe a view"""
        resultados = self.dao.listar_todos_orcamentos()
        orcamentos = []

        for r in resultados:
            o = Orcamento(
                cliente_id=r['cliente_id'],
                veiculo_id=r['veiculo_id'],
                descricao=r['descricao'],
                valor_estimado=r['valor_estimado'],
                validade=r['validade'],
                estado=r['estado'],
                id=r['id'],
                data_criacao=r.get('data_criacao')
            )
            o.cliente_nome = r.get('cliente_nome')
            o.veiculo_marca = r.get('veiculo_marca')
            o.veiculo_modelo = r.get('veiculo_modelo')
            orcamentos.append(o)

        self.view = OrcamentoView(orcamentos, self)
        self.view.show()

    def criar_orcamento(self, cliente_id, veiculo_id, descricao, valor_estimado, validade, estado="pendente"):
        orcamento = Orcamento(cliente_id, veiculo_id, descricao, valor_estimado, validade, estado)
        orcamento_id = self.dao.criar_orcamento(orcamento)
        if orcamento_id:
            self.iniciar()

    def editar_orcamento(self, orcamento: Orcamento):
        """Atualiza orçamento e cria folha se aprovado"""
        sucesso = self.dao.atualizar_orcamento(orcamento)
        if sucesso:
            logging.info(f"Orçamento {orcamento.id} atualizado com estado '{orcamento.estado}'")
            # Se o orçamento passou a aprovado, cria a folha de serviço automaticamente
            if orcamento.estado == "aprovado":
                self._criar_folha_servico(orcamento)
            self.iniciar()

    def _criar_folha_servico(self, orcamento: Orcamento):
        """Cria automaticamente a folha de serviço associada ao orçamento aprovado"""
        folha = {
            "orcamento_id": orcamento.id,
            "cliente_id": orcamento.cliente_id,
            "veiculo_id": orcamento.veiculo_id,
            "descricao_servico": orcamento.descricao,
            "estado": "pendente",
            "tempo_real": 0
        }
        sucesso = self.fs_dao.criar_folha_servico(folha)
        if sucesso:
            logging.info(f"Folha de serviço criada automaticamente para o orçamento {orcamento.id}")
        else:
            logging.error(f"Falha ao criar folha de serviço para o orçamento {orcamento.id}")

    def eliminar_orcamento(self, orcamento_id):
        sucesso = self.dao.eliminar_orcamento(orcamento_id)
        if sucesso:
            self.iniciar()

    def exportar_pdf_orcamento(self, orcamento: Orcamento):
        """Exporta um orçamento específico para PDF"""
        filename = f"Orcamento_{orcamento.id}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height-50, f"Orçamento #{orcamento.id}")
        c.setFont("Helvetica", 12)
        c.drawString(50, height-80, f"Cliente: {orcamento.cliente_nome}")
        c.drawString(50, height-100, f"Veículo: {orcamento.veiculo_marca} {orcamento.veiculo_modelo}")
        c.drawString(50, height-120, f"Valor Estimado: {orcamento.valor_estimado}")
        c.drawString(50, height-140, f"Validade: {orcamento.validade}")
        c.drawString(50, height-160, f"Estado: {orcamento.estado}")
        c.drawString(50, height-180, "Descrição:")
        c.setFont("Helvetica", 10)

        y = height-200
        for linha in orcamento.descricao.split("\n"):
            c.drawString(60, y, linha)
            y -= 15

        c.save()
        logging.info(f"Orçamento exportado para {filename}")
