from View.FolhaServicoView import FolhaServicoView
from DAO.FolhaServicoDAO import FolhaServicoDAO
from DAO.RegistoTempoDAO import RegistoTempoDAO
from PyQt5.QtWidgets import QMessageBox
import logging

# Configuração de logging
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

    def iniciar(self):
        """Método para iniciar a view e carregar as folhas de serviço."""
        self.atualizar_tabela_folhas()
        self.view.exec_()
    
    def atualizar_tabela_folhas(self):
        """Atualiza a tabela de folhas de serviço com dados mais recentes."""
        folhas = self.fs_dao.obter_todas_folhas_servico()
        self.view.popular_tabela(folhas)

    def verificar_estado_servico(self, folha_id):
        """Verifica o estado da folha de serviço e retorna um estado"""
        folha = self.fs_dao.obter_folha_por_id(folha_id)
        if folha:
            return folha['estado']
        return None

    def iniciar_servico(self):
        """Inicia o serviço, atualizando o estado na base de dados."""
        folha_id = self.view.obter_linha_selecionada_id()
        if folha_id:
            estado = self.verificar_estado_servico(folha_id)
            if estado == 'pendente':
                if self.rt_dao.iniciar_registo_tempo(folha_id, self.utilizador_id):
                    self.view.mostrar_mensagem("Sucesso", "Serviço iniciado com sucesso.")
                    logging.info(f"Serviço iniciado para a folha de serviço ID: {folha_id}")
                    self.atualizar_tabela_folhas()
                else:
                    self.view.mostrar_mensagem("Erro", "Falha ao iniciar o serviço.")
                    logging.error(f"Falha ao iniciar serviço para a folha de serviço ID: {folha_id}")
            else:
                self.view.mostrar_mensagem("Erro", "O serviço já está em progresso ou foi concluído.")
        else:
            self.view.mostrar_mensagem("Erro", "Selecione uma folha de serviço para iniciar.")
            logging.warning("Nenhuma folha de serviço selecionada para iniciar.")

    def finalizar_servico(self):
        """Finaliza o serviço, registrando o tempo e finalizando o processo."""
        folha_id = self.view.obter_linha_selecionada_id()
        if folha_id:
            estado = self.verificar_estado_servico(folha_id)
            if estado == 'em_progresso':
                if self.rt_dao.finalizar_registo_tempo(folha_id):
                    self.view.mostrar_mensagem("Sucesso", "Serviço finalizado com sucesso.")
                    logging.info(f"Serviço finalizado para a folha de serviço ID: {folha_id}")
                    self.atualizar_tabela_folhas()
                else:
                    self.view.mostrar_mensagem("Erro", "Falha ao finalizar o serviço.")
                    logging.error(f"Falha ao finalizar serviço para a folha de serviço ID: {folha_id}")
            else:
                self.view.mostrar_mensagem("Erro", "O serviço não está em progresso.")
                logging.warning(f"Tentativa de finalizar um serviço que não está em progresso (ID: {folha_id}).")
        else:
            self.view.mostrar_mensagem("Erro", "Selecione uma folha de serviço para finalizar.")
            logging.warning("Nenhuma folha de serviço selecionada para finalizar.")

    def apagar_folha_servico(self):
        """Apaga a folha de serviço selecionada da base de dados."""
        folha_id = self.view.obter_linha_selecionada_id()
        if folha_id:
            confirmar = QMessageBox.question(self.view, 'Confirmação', 
                                             "Tem certeza que deseja apagar esta folha de serviço?", 
                                             QMessageBox.Yes | QMessageBox.No)
            if confirmar == QMessageBox.Yes:
                if self.fs_dao.excluir_folha_servico(folha_id):
                    self.view.mostrar_mensagem("Sucesso", "Folha de serviço apagada com sucesso.")
                    logging.info(f"Folha de serviço ID: {folha_id} apagada com sucesso.")
                    self.atualizar_tabela_folhas()
                else:
                    self.view.mostrar_mensagem("Erro", "Falha ao apagar folha de serviço.")
                    logging.error(f"Falha ao apagar folha de serviço ID: {folha_id}")
        else:
            self.view.mostrar_mensagem("Erro", "Selecione uma folha de serviço para apagar.")
            logging.warning("Nenhuma folha de serviço selecionada para apagar.")
