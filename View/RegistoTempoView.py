# View/RegistoTempoView.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt

class RegistoTempoView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registos de Tempo")
        self.resize(700, 400)

        main_layout = QVBoxLayout()

        # Tabela de registos de tempo
        self.tabela_registos = QTableWidget()
        self.tabela_registos.setColumnCount(4)
        self.tabela_registos.setHorizontalHeaderLabels([
            "ID", "Início", "Fim", "Utilizador"
        ])
        # Ajuste de larguras
        self.tabela_registos.setColumnWidth(0, 50)   # ID
        self.tabela_registos.setColumnWidth(1, 150)  # Início
        self.tabela_registos.setColumnWidth(2, 150)  # Fim
        self.tabela_registos.setColumnWidth(3, 200)  # Utilizador
        main_layout.addWidget(self.tabela_registos)

        # Botão fechar
        btn_layout = QHBoxLayout()
        self.btn_fechar = QPushButton("Fechar")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_fechar)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Conectar botão fechar
        self.btn_fechar.clicked.connect(self.close)

    def popular_tabela(self, registos):
        """Preenche a tabela com os registos de tempo"""
        self.tabela_registos.setRowCount(len(registos))
        for i, r in enumerate(registos):
            self.tabela_registos.setItem(i, 0, QTableWidgetItem(str(r.get('id', ''))))
            self.tabela_registos.setItem(i, 1, QTableWidgetItem(str(r.get('inicio', ''))))
            self.tabela_registos.setItem(i, 2, QTableWidgetItem(str(r.get('fim', ''))))
            self.tabela_registos.setItem(i, 3, QTableWidgetItem(str(r.get('utilizador_nome', ''))))
