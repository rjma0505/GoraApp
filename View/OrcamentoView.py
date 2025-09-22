# View/OrcamentoView.py

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLabel

class OrcamentoView(QMainWindow):
    def __init__(self, orcamentos, controller, parent=None):
        """Construtor da OrcamentoView"""
        super().__init__(parent)
        self.setWindowTitle("Orçamentos")
        
        self.orcamentos = orcamentos  # Lista de orçamentos a serem exibidos
        self.controller = controller  # Passa o controlador para a view
        
        # Defina o layout da janela
        layout = QVBoxLayout()

        # Adiciona um rótulo para exibir se não houver orçamentos
        if not orcamentos:
            self.no_orcamentos_label = QLabel("Nenhum orçamento encontrado.")
            layout.addWidget(self.no_orcamentos_label)  # Exibe a mensagem
            
            # Aqui você pode abrir o CriarOrcamentoDialog automaticamente se não houver orçamentos
            self.abrir_criar_orcamento_dialog()
        
        # Crie uma tabela para exibir os orçamentos, se houver
        self.table_widget = QTableWidget()
        
        if orcamentos:
            self.table_widget.setRowCount(len(orcamentos))  # Defina o número de linhas
            self.table_widget.setColumnCount(5)  # Defina o número de colunas (ajuste conforme necessário)

            # Preencha a tabela com os dados
            for row, orcamento in enumerate(orcamentos):
                self.table_widget.setItem(row, 0, QTableWidgetItem(str(orcamento.id)))  # Exemplo de preenchimento
                self.table_widget.setItem(row, 1, QTableWidgetItem(orcamento.cliente_nome))
                self.table_widget.setItem(row, 2, QTableWidgetItem(orcamento.veiculo_info))
                self.table_widget.setItem(row, 3, QTableWidgetItem(str(orcamento.valor_estimado)))
                self.table_widget.setItem(row, 4, QTableWidgetItem(orcamento.estado))

            layout.addWidget(self.table_widget)
        
        # Botão para criar novo orçamento
        self.criar_orcamento_button = QPushButton("Criar Novo Orçamento")
        self.criar_orcamento_button.clicked.connect(self.criar_orcamento)
        
        layout.addWidget(self.criar_orcamento_button)
        
        # Defina o layout principal
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def criar_orcamento(self):
        """Abre a janela para criar um novo orçamento"""
        from View.CriarOrcamentoDialog import CriarOrcamentoDialog  # Importação aqui para evitar o loop circular
        dialog = CriarOrcamentoDialog(self.controller)  # Passando a instância de OrcamentoController para a view
        dialog.exec_()

    def abrir_criar_orcamento_dialog(self):
        """Abre o diálogo de criação de orçamento automaticamente"""
        from View.CriarOrcamentoDialog import CriarOrcamentoDialog  # Importação aqui para evitar o loop circular
        dialog = CriarOrcamentoDialog(self.controller)  # Passando o controlador para o dialog
        dialog.exec_()

    def show_window(self):
        """Mostra a janela"""
        print("Abrindo OrcamentoView...")  # Depuração
        if not self.orcamentos:  # Verifica se não há orçamentos
            self.abrir_criar_orcamento_dialog()  # Abre o diálogo automaticamente

        self.show()  # Exibe a janela da OrcamentoView
