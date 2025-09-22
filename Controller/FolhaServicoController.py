# Controller/FolhaServicoController.py

from View.FolhaServicoView import FolhaServicoView
from DAO.FolhaServicoDAO import FolhaServicoDAO
from DAO.RegistoTempoDAO import RegistoTempoDAO
from PyQt5.QtWidgets import QMessageBox
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FolhaServicoController:
    def __init__(self, utilizador_id):
        self.view = FolhaServicoView()
        self.fs_dao = FolhaServicoDAO()
        self.rt_dao = RegistoTempoDAO()
        self.utilizador_id = utilizador_id

        # Conectar eventos dos botões
        self.view.btn_iniciar.clicked.connect(self.iniciar_servico)
        self.view.btn_finalizar.clicked.connect(self.finalizar_servico)
        self.view.btn_apagar.clicked.connect(self.apagar_folha_servico)
        self.view.btn_historico.clicked.connect(self.ver_registos_tempo)

    def iniciar(self):
        """Abre a view e carrega as folhas aprovadas"""
        self.atualizar_tabela_folhas()
        self.view.exec_()

    def atualizar_tabela_folhas(self):
        """Carrega apenas folhas de orçamentos aprovados"""
        folhas = self.fs_dao.obter_folhas_aprovadas()
        self.view.popular_tabela(folhas)

    def verificar_estado_servico(self, folha_id):
        folha = self.fs_dao.obter_folha_por_id(folha_id)
        if folha:
            return folha['estado']
        return None

    def iniciar_servico(self):
        folha_id = self.view.obter_linha_selecionada_id()
        if not folha_id:
            self.view.mostrar_mensagem("Erro", "Selecione uma folha de serviço para iniciar.")
            return

        estado = self.verificar_estado_servico(folha_id)
        if estado != "pendente":
            self.view.mostrar_mensagem("Erro", "O serviço já foi iniciado ou finalizado.")
            return

        if self.rt_dao.iniciar_registo_tempo(folha_id, self.utilizador_id):
            logging.info(f"Serviço iniciado na folha {folha_id}")
            self.view.mostrar_mensagem("Sucesso", "Serviço iniciado com sucesso.")
            self.fs_dao.atualizar_folha_servico({
                'id': folha_id,
                'descricao_servico': self.fs_dao.obter_folha_por_id(folha_id)['descricao_servico'],
                'estado': 'em_progresso',
                'tempo_real': self.fs_dao.obter_folha_por_id(folha_id)['tempo_real'] or 0
            })
            self.atualizar_tabela_folhas()
        else:
            self.view.mostrar_mensagem("Erro", "Já existe um registo de tempo ativo para esta folha.")

    def finalizar_servico(self):
        folha_id = self.view.obter_linha_selecionada_id()
        if not folha_id:
            self.view.mostrar_mensagem("Erro", "Selecione uma folha de serviço para finalizar.")
            return

        estado = self.verificar_estado_servico(folha_id)
        if estado != "em_progresso":
            self.view.mostrar_mensagem("Erro", "O serviço não está em progresso.")
            return

        if self.rt_dao.finalizar_registo_tempo(folha_id):
            logging.info(f"Serviço finalizado na folha {folha_id}")
            self.view.mostrar_mensagem("Sucesso", "Serviço finalizado com sucesso.")
            # Atualizar estado para efetuado
            self.fs_dao.atualizar_folha_servico({
                'id': folha_id,
                'descricao_servico': self.fs_dao.obter_folha_por_id(folha_id)['descricao_servico'],
                'estado': 'efetuado',
                'tempo_real': self.fs_dao.obter_folha_por_id(folha_id)['tempo_real'] or 0
            })
            self.atualizar_tabela_folhas()
        else:
            self.view.mostrar_mensagem("Erro", "Falha ao finalizar o serviço.")

    def apagar_folha_servico(self):
        folha_id = self.view.obter_linha_selecionada_id()
        if not folha_id:
            self.view.mostrar_mensagem("Erro", "Selecione uma folha de serviço para apagar.")
            return

        confirm = QMessageBox.question(self.view, "Apagar Folha",
                                       f"Deseja realmente apagar a folha de serviço {folha_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if self.fs_dao.excluir_folha_servico(folha_id):
                logging.info(f"Folha {folha_id} apagada")
                self.view.mostrar_mensagem("Sucesso", "Folha de serviço apagada com sucesso.")
                self.atualizar_tabela_folhas()
            else:
                self.view.mostrar_mensagem("Erro", "Falha ao apagar a folha de serviço.")

    def ver_registos_tempo(self):
        folha_id = self.view.obter_linha_selecionada_id()
        if not folha_id:
            self.view.mostrar_mensagem("Erro", "Selecione uma folha de serviço.")
            return

        from Controller.RegistoTempoController import RegistoTempoController
        controller = RegistoTempoController(folha_id)
        controller.iniciar()
