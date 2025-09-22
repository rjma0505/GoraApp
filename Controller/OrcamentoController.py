# Controller/OrcamentoController.py

from DAO.OrcamentoDAO import OrcamentoDAO
from DAO.FolhaServicoDAO import FolhaServicoDAO
from Model.Orcamento import Orcamento
from View.OrcamentoView import OrcamentoView
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class OrcamentoController:
    def __init__(self):
        self.dao = OrcamentoDAO()
        self.folha_servico_dao = FolhaServicoDAO()
        self.view = None

    def iniciar(self):
        """Carrega todos os orçamentos e exibe na view"""
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
            # Adiciona nomes/marcas para exibição
            o.cliente_nome = r.get('cliente_nome')
            o.veiculo_marca = r.get('veiculo_marca')
            o.veiculo_modelo = r.get('veiculo_modelo')
            orcamentos.append(o)

        self.view = OrcamentoView(orcamentos, self)
        self.view.show()

    def criar_orcamento(self, cliente_id, veiculo_id, descricao, valor_estimado, validade, estado="pendente"):
        """Cria um novo orçamento"""
        orcamento = Orcamento(cliente_id, veiculo_id, descricao, valor_estimado, validade, estado)
        orcamento_id = self.dao.criar_orcamento(orcamento)
        if orcamento_id:
            self.iniciar()

    def editar_orcamento(self, orcamento: Orcamento):
        """Atualiza um orçamento existente"""
        sucesso = self.dao.atualizar_orcamento(orcamento)
        if sucesso:
            # Se o orçamento for aprovado, cria automaticamente uma folha de serviço
            if orcamento.estado == "aprovado":
                folha_id = self.folha_servico_dao.criar_folha_de_orcamento(orcamento.id)
                if folha_id:
                    print(f"Folha de serviço criada automaticamente! ID: {folha_id}")
            self.iniciar()

    def eliminar_orcamento(self, orcamento_id):
        """Elimina um orçamento pelo ID"""
        sucesso = self.dao.eliminar_orcamento(orcamento_id)
        if sucesso:
            self.iniciar()

    def exportar_pdf_orcamento(self, orcamento_id):
        """Exporta um orçamento específico para PDF"""
        # Obter o orçamento correto
        resultados = self.dao.listar_todos_orcamentos()
        orc = next((r for r in resultados if r['id'] == orcamento_id), None)
        if not orc:
            print("Orçamento não encontrado para exportar")
            return

        filename = f"Orcamento_{orc['id']}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height-50, f"Orçamento #{orc['id']}")
        c.setFont("Helvetica", 12)
        c.drawString(50, height-80, f"Cliente: {orc['cliente_nome']}")
        c.drawString(50, height-100, f"Veículo: {orc['veiculo_marca']} {orc['veiculo_modelo']}")
        c.drawString(50, height-120, f"Valor Estimado: {orc['valor_estimado']}")
        c.drawString(50, height-140, f"Validade: {orc['validade']}")
        c.drawString(50, height-160, f"Estado: {orc['estado']}")
        c.drawString(50, height-180, "Descrição:")
        c.setFont("Helvetica", 10)

        y = height-200
        for linha in orc['descricao'].split("\n"):
            c.drawString(60, y, linha)
            y -= 15

        c.save()
        print(f"Orçamento exportado para {filename}")
