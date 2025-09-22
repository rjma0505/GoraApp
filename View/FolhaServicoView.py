from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog

class FolhaServicoView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestão de Folhas de Serviço")
        self.resize(800, 600)
        
        main_layout = QVBoxLayout()
        
        self.tabela_folhas = QTableWidget()
        self.tabela_folhas.setColumnCount(5)
        self.tabela_folhas.setHorizontalHeaderLabels(["ID", "Matrícula", "Descrição", "Estado", "Tempo Real"])
        self.tabela_folhas.setColumnWidth(2, 250)
        main_layout.addWidget(self.tabela_folhas)
        
        # Botões de Ação
        self.btn_iniciar = QPushButton("Iniciar Serviço")
        self.btn_finalizar = QPushButton("Finalizar Serviço")
        self.btn_apagar = QPushButton("Apagar Folha")
        
        main_layout.addWidget(self.btn_iniciar)
        main_layout.addWidget(self.btn_finalizar)
        main_layout.addWidget(self.btn_apagar)
        
        self.setLayout(main_layout)

        # Conectar os botões às funções
        self.btn_iniciar.clicked.connect(self.iniciar_servico)
        self.btn_finalizar.clicked.connect(self.finalizar_servico)
        self.btn_apagar.clicked.connect(self.apagar_folha)

        # Desabilitar os botões até que uma linha seja selecionada
        self.btn_finalizar.setEnabled(False)
        self.btn_apagar.setEnabled(False)
        self.btn_iniciar.setEnabled(False)

        # Conectar a seleção da tabela para habilitar/desabilitar os botões
        self.tabela_folhas.currentItemChanged.connect(self.atualizar_botoes)

    def popular_tabela(self, folhas):
        """Preenche a tabela com as folhas de serviço."""
        self.tabela_folhas.setRowCount(len(folhas))
        for i, folha in enumerate(folhas):
            self.tabela_folhas.setItem(i, 0, QTableWidgetItem(str(folha.get('id', ''))))
            self.tabela_folhas.setItem(i, 1, QTableWidgetItem(folha.get('matricula', '')))
            self.tabela_folhas.setItem(i, 2, QTableWidgetItem(folha.get('descricao_servico', '')))
            self.tabela_folhas.setItem(i, 3, QTableWidgetItem(folha.get('estado', '')))
            self.tabela_folhas.setItem(i, 4, QTableWidgetItem(str(folha.get('tempo_real', ''))))

    def obter_linha_selecionada_id(self):
        """Obtém o ID da folha de serviço selecionada."""
        linha = self.tabela_folhas.currentRow()
        if linha >= 0:
            return int(self.tabela_folhas.item(linha, 0).text())
        return None

    def atualizar_botoes(self):
        """Habilita ou desabilita os botões conforme a seleção de uma folha."""
        if self.tabela_folhas.currentItem():
            self.btn_iniciar.setEnabled(True)
            self.btn_finalizar.setEnabled(True)
            self.btn_apagar.setEnabled(True)
        else:
            self.btn_iniciar.setEnabled(False)
            self.btn_finalizar.setEnabled(False)
            self.btn_apagar.setEnabled(False)

    def iniciar_servico(self):
        """Inicia o serviço da folha de serviço selecionada."""
        folha_id = self.obter_linha_selecionada_id()
        if not folha_id:
            self.mostrar_mensagem("Erro", "Selecione uma folha de serviço para iniciar.")
            return

        # Lógica para iniciar o serviço (alterar estado no banco de dados, etc.)
        self.mostrar_mensagem("Serviço Iniciado", f"A folha de serviço {folha_id} foi iniciada com sucesso.")
        self.atualizar_tabela()

    def finalizar_servico(self):
        """Finaliza o serviço da folha de serviço selecionada."""
        folha_id = self.obter_linha_selecionada_id()
        if not folha_id:
            self.mostrar_mensagem("Erro", "Selecione uma folha de serviço para finalizar.")
            return

        # Lógica para finalizar o serviço (alterar estado no banco de dados, etc.)
        tempo_real, ok = QInputDialog.getInt(self, "Tempo Real", "Digite o tempo real gasto:", min=0)
        if ok:
            # Atualiza o tempo real e o estado da folha
            self.mostrar_mensagem("Serviço Finalizado", f"A folha de serviço {folha_id} foi finalizada. Tempo real: {tempo_real} minutos.")
            self.atualizar_tabela()

    def apagar_folha(self):
        """Apaga a folha de serviço selecionada."""
        folha_id = self.obter_linha_selecionada_id()
        if not folha_id:
            self.mostrar_mensagem("Erro", "Selecione uma folha de serviço para apagar.")
            return

        resposta = QMessageBox.question(self, "Apagar Folha", f"Deseja realmente apagar a folha de serviço {folha_id}?", 
                                        QMessageBox.Yes | QMessageBox.No)
        if resposta == QMessageBox.Yes:
            # Lógica para apagar a folha de serviço (remover do banco de dados, etc.)
            self.mostrar_mensagem("Folha Apagada", f"A folha de serviço {folha_id} foi apagada com sucesso.")
            self.atualizar_tabela()

    def atualizar_tabela(self):
        """Atualiza a tabela de folhas de serviço."""
        # Lógica para buscar as folhas de serviço atualizadas do banco de dados
        folhas = []  # Substitua isso pela lista atualizada de folhas
        self.popular_tabela(folhas)

    def mostrar_mensagem(self, titulo, mensagem):
        """Exibe uma mensagem de alerta."""
        QMessageBox.information(self, titulo, mensagem)
