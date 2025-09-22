# View/VeiculoView.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QListWidget, QHBoxLayout, QLabel, QMessageBox

class VeiculoView(QDialog):
    def __init__(self, clientes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestão de Veículos")
        self.resize(600, 400)
        self.clientes = clientes

        main_layout = QVBoxLayout()
        
        self.lista_veiculos = QListWidget()
        main_layout.addWidget(QLabel("Lista de Veículos:"))
        main_layout.addWidget(self.lista_veiculos)

        self.btn_criar = QPushButton("Adicionar Veículo")
        self.btn_editar = QPushButton("Editar Veículo")
        self.btn_apagar = QPushButton("Apagar Veículo")
        main_layout.addWidget(self.btn_criar)
        main_layout.addWidget(self.btn_editar)
        main_layout.addWidget(self.btn_apagar)

        self.setLayout(main_layout)

    def popular_lista(self, veiculos):
        self.lista_veiculos.clear()
        for v in veiculos:
            self.lista_veiculos.addItem(f"{v.id}: {v.matricula} ({v.marca} {v.modelo}) - {v.pais}")

    def mostrar_mensagem(self, titulo, mensagem):
        QMessageBox.information(self, titulo, mensagem)

    def obter_veiculo_selecionado_id(self):
        item = self.lista_veiculos.currentItem()
        if item:
            return int(item.text().split(":")[0])
        return None
