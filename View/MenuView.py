# View/MenuView.py

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class MenuView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.utilizador = None
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Menu Principal")
        self.resize(700, 450)

        # Outer widget + layout para centralizar
        outer = QWidget()
        outer_layout = QHBoxLayout(outer)
        outer_layout.setContentsMargins(30, 30, 30, 30)
        outer_layout.setAlignment(Qt.AlignCenter)

        # Painel central
        panel = QWidget()
        panel.setFixedWidth(420)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(12)
        panel_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Título
        self.lbl_titulo = QLabel("Menu Principal")
        self.lbl_titulo.setFont(QFont("Sans Serif", 18, QFont.Bold))
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setWordWrap(True)  # Permite quebra de linha
        self.lbl_titulo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Botões
        self.btn_orcamentos = QPushButton("📑 Orçamentos")
        self.btn_folhas_servico = QPushButton("🛠️ Folhas de Serviço")
        self.btn_clientes = QPushButton("👤 Clientes")
        self.btn_veiculos = QPushButton("🚗 Veículos")

        # Estilo comum dos botões
        for btn in (self.btn_orcamentos, self.btn_folhas_servico, self.btn_clientes, self.btn_veiculos):
            btn.setMinimumHeight(46)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1976D2;
                    color: white;
                    border-radius: 8px;
                    font-size: 14px;
                    padding: 8px 12px;
                }
                QPushButton:hover { background-color: #1565C0; }
                QPushButton:disabled { background-color: #B0BEC5; color: #ECEFF1; }
            """)

        # Montar layout
        panel_layout.addWidget(self.lbl_titulo)
        panel_layout.addSpacerItem(QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))
        panel_layout.addWidget(self.btn_orcamentos)
        panel_layout.addWidget(self.btn_folhas_servico)
        panel_layout.addWidget(self.btn_clientes)
        panel_layout.addWidget(self.btn_veiculos)
        panel_layout.addSpacerItem(QSpacerItem(20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding))

        outer_layout.addWidget(panel)
        self.setCentralWidget(outer)

        # Centralizar na tela após exibir
        QTimer.singleShot(0, self._center_on_screen)

    def set_utilizador(self, utilizador):
        """Define o utilizador autenticado e atualiza a interface"""
        self.utilizador = utilizador
        if utilizador:
            self.setWindowTitle(f"Menu - {utilizador.username} ({utilizador.role})")
            self.lbl_titulo.setText(f"Bem-vindo, {utilizador.username}!")

    def _center_on_screen(self):
        """Centraliza a janela na tela"""
        screen = self.screen()
        if not screen:
            return
        center = screen.availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(center)
        self.move(frame.topLeft())
