from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class MenuView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.utilizador = None  # Inicializa como None, pois será configurado depois
        self.init_ui()

    def init_ui(self):
        # Aqui você configura a interface gráfica da sua janela
        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 100, 800, 600)
        
        # Criar os botões para interação
        self.btn_orcamentos = QPushButton("Orçamentos")
        self.btn_folhas_servico = QPushButton("Folhas de Serviço")
        self.btn_clientes = QPushButton("Clientes")
        self.btn_veiculos = QPushButton("Veículos")
        
        # Layout para adicionar os botões
        layout = QVBoxLayout()
        layout.addWidget(self.btn_orcamentos)
        layout.addWidget(self.btn_folhas_servico)
        layout.addWidget(self.btn_clientes)
        layout.addWidget(self.btn_veiculos)
        
        # Container de widget para a centralização do layout
        container = QWidget()
        container.setLayout(layout)
        
        # Definir o container como o central widget
        self.setCentralWidget(container)

    def set_utilizador(self, utilizador):
        """
        Define o utilizador que foi autenticado.
        """
        self.utilizador = utilizador
        # Exemplo: você pode atualizar a interface com o nome do utilizador, se necessário
        self.update_ui_based_on_role()

    def update_ui_based_on_role(self):
        """
        Atualiza a interface de acordo com o papel (role) do utilizador.
        """
        if self.utilizador and self.utilizador.role:
            # Exemplo: Mostra o nome do utilizador na interface ou faz ajustes na UI
            self.setWindowTitle(f"Menu - {self.utilizador.username} ({self.utilizador.role})")
            # Atualizações adicionais com base no papel, se necessário
