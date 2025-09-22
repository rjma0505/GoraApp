# View/FolhaServicoView.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt

class FolhaServicoView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestão de Folhas de Serviço")
        self.resize(1000, 600)

        main_layout = QVBoxLayout()

        # Tabela de folhas de serviço
        self.tabela_folhas = QTableWidget()
        self.tabela_folhas.setColumnCount(8)
        self.tabela_folhas.setHorizontalHeaderLabels([
            "ID", "Cliente", "Veículo", "Descrição", "Estado", 
            "Tempo Real", "Orçamento", "Registos Tempo"
        ])
        # Ajuste de larguras
        self.tabela_folhas.setColumnWidth(0, 50)   # ID
        self.tabela_folhas.setColumnWidth(1, 150)  # Cliente
        self.tabela_folhas.setColumnWidth(2, 200)  # Veículo
        self.tabela_folhas.setColumnWidth(3, 300)  # Descrição
        self.tabela_folhas.setColumnWidth(4, 100)  # Estado
        self.tabela_folhas.setColumnWidth(5, 100)  # Tempo Real
        self.tabela_folhas.setColumnWidth(6, 80)   # Orçamento
        self.tabela_folhas.setColumnWidth(7, 120)  # Registos Tempo
        main_layout.addWidget(self.tabela_folhas)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_iniciar = QPushButton("Iniciar Serviço")
        self.btn_finalizar = QPushButton("Finalizar Serviço")
        self.btn_apagar = QPushButton("Apagar Folha")
        self.btn_historico = QPushButton("Ver Registos de Tempo")
        btn_layout.addWidget(self.btn_iniciar)
        btn_layout.addWidget(self.btn_finalizar)
        btn_layout.addWidget(self.btn_apagar)
        btn_layout.addWidget(self.btn_historico)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Inicialmente desabilitar botões
        self.btn_iniciar.setEnabled(False)
        self.btn_finalizar.setEnabled(False)
        self.btn_apagar.setEnabled(False)
        self.btn_historico.setEnabled(False)

        # Conectar seleção da tabela
        self.tabela_folhas.currentItemChanged.connect(self.atualizar_botoes)

    def popular_tabela(self, folhas):
        """Preenche a tabela com dados das folhas de serviço"""
        self.tabela_folhas.setRowCount(len(folhas))
        for i, f in enumerate(folhas):
            # ID
            self.tabela_folhas.setItem(i, 0, QTableWidgetItem(str(f.get('id', ''))))
            # Cliente
            self.tabela_folhas.setItem(i, 1, QTableWidgetItem(f.get('cliente_nome', '')))
            # Veículo
            veiculo_str = f"{f.get('veiculo_marca','')} {f.get('veiculo_modelo','')} ({f.get('matricula','')})"
            self.tabela_folhas.setItem(i, 2, QTableWidgetItem(veiculo_str))
            # Descrição
            self.tabela_folhas.setItem(i, 3, QTableWidgetItem(f.get('descricao_servico', '')))
            # Estado
            self.tabela_folhas.setItem(i, 4, QTableWidgetItem(f.get('estado', '')))
            # Tempo real formatado hh:mm
            tempo_min = f.get('tempo_real', 0) or 0
            h = tempo_min // 60
            m = tempo_min % 60
            tempo_str = f"{h:02d}:{m:02d}"
            self.tabela_folhas.setItem(i, 5, QTableWidgetItem(tempo_str))
            # Orçamento
            self.tabela_folhas.setItem(i, 6, QTableWidgetItem(str(f.get('orcamento_id',''))))
            # Registos tempo (ativo ou qtd.)
            registos_info = "Ativo" if f.get('registo_ativo', False) else str(f.get('qtd_registos', 0))
            self.tabela_folhas.setItem(i, 7, QTableWidgetItem(registos_info))

    def obter_linha_selecionada_id(self):
        linha = self.tabela_folhas.currentRow()
        if linha >= 0:
            return int(self.tabela_folhas.item(linha, 0).text())
        return None

    def atualizar_botoes(self):
        if self.tabela_folhas.currentItem():
            self.btn_iniciar.setEnabled(True)
            self.btn_finalizar.setEnabled(True)
            self.btn_apagar.setEnabled(True)
            self.btn_historico.setEnabled(True)
        else:
            self.btn_iniciar.setEnabled(False)
            self.btn_finalizar.setEnabled(False)
            self.btn_apagar.setEnabled(False)
            self.btn_historico.setEnabled(False)

    def mostrar_mensagem(self, titulo, mensagem):
        QMessageBox.information(self, titulo, mensagem)
