from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QFormLayout, QLineEdit, QMessageBox

class VeiculoView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestão de Veículos")
        self.resize(600, 400)

        main_layout = QVBoxLayout()
        
        # Lista de veículos
        self.lista_veiculos = QListWidget()
        main_layout.addWidget(self.lista_veiculos)
        
        # Formulário para dados do veículo
        form_layout = QFormLayout()
        self.input_cliente_id = QLineEdit()
        self.input_marca = QLineEdit()
        self.input_modelo = QLineEdit()
        self.input_matricula = QLineEdit()
        self.input_pais = QLineEdit()
        form_layout.addRow("ID Cliente:", self.input_cliente_id)
        form_layout.addRow("Marca:", self.input_marca)
        form_layout.addRow("Modelo:", self.input_modelo)
        form_layout.addRow("Matrícula:", self.input_matricula)
        form_layout.addRow("País:", self.input_pais)
        main_layout.addLayout(form_layout)

        # Botões de ação
        self.btn_criar = QPushButton("Adicionar Veículo")
        self.btn_editar = QPushButton("Salvar Edição")
        self.btn_apagar = QPushButton("Apagar Veículo")
        
        # Estilização dos botões
        self.btn_criar.setStyleSheet("font-size: 14px; padding: 10px;")
        self.btn_editar.setStyleSheet("font-size: 14px; padding: 10px;")
        self.btn_apagar.setStyleSheet("font-size: 14px; padding: 10px;")
        
        main_layout.addWidget(self.btn_criar)
        main_layout.addWidget(self.btn_editar)
        main_layout.addWidget(self.btn_apagar)
        
        self.setLayout(main_layout)

        # Conectar os botões às funções
        self.btn_criar.clicked.connect(self.adicionar_veiculo)
        self.btn_editar.clicked.connect(self.editar_veiculo)
        self.btn_apagar.clicked.connect(self.apagar_veiculo)

    def popular_lista(self, veiculos):
        """Preenche a lista de veículos."""
        self.lista_veiculos.clear()
        for veiculo in veiculos:
            self.lista_veiculos.addItem(f"{veiculo.id}: {veiculo.matricula} ({veiculo.marca} {veiculo.modelo})")
    
    def obter_dados_formulario(self):
        """Obtém os dados inseridos no formulário."""
        return {
            "cliente_id": self.input_cliente_id.text(),
            "marca": self.input_marca.text(),
            "modelo": self.input_modelo.text(),
            "matricula": self.input_matricula.text(),
            "pais": self.input_pais.text()
        }
    
    def limpar_formulario(self):
        """Limpa o formulário de dados do veículo."""
        self.input_cliente_id.clear()
        self.input_marca.clear()
        self.input_modelo.clear()
        self.input_matricula.clear()
        self.input_pais.clear()
    
    def mostrar_mensagem(self, titulo, mensagem):
        """Exibe uma mensagem para o usuário."""
        QMessageBox.information(self, titulo, mensagem)

    def obter_veiculo_selecionado_id(self):
        """Obtém o ID do veículo selecionado na lista."""
        item = self.lista_veiculos.currentItem()
        if item:
            return int(item.text().split(':')[0])
        return None

    def adicionar_veiculo(self):
        """Adiciona um novo veículo usando os dados do formulário."""
        dados = self.obter_dados_formulario()
        
        # Validar campos
        if not all(dados.values()):
            self.mostrar_mensagem("Erro", "Por favor, preencha todos os campos.")
            return
        
        # Lógica para adicionar o veículo
        # Aqui você pode chamar a lógica de inserção no banco de dados ou outro processamento
        self.mostrar_mensagem("Veículo Adicionado", f"Veículo {dados['matricula']} adicionado com sucesso!")
        self.limpar_formulario()
        self.atualizar_lista_veiculos()

    def editar_veiculo(self):
        """Edita o veículo selecionado na lista."""
        veiculo_id = self.obter_veiculo_selecionado_id()
        if not veiculo_id:
            self.mostrar_mensagem("Erro", "Selecione um veículo para editar.")
            return
        
        dados = self.obter_dados_formulario()

        # Validar campos
        if not all(dados.values()):
            self.mostrar_mensagem("Erro", "Por favor, preencha todos os campos.")
            return
        
        # Lógica para editar o veículo
        # Aqui você pode chamar a lógica de atualização no banco de dados ou outro processamento
        self.mostrar_mensagem("Veículo Editado", f"Veículo {dados['matricula']} editado com sucesso!")
        self.limpar_formulario()
        self.atualizar_lista_veiculos()

    def apagar_veiculo(self):
        """Apaga o veículo selecionado na lista."""
        veiculo_id = self.obter_veiculo_selecionado_id()
        if not veiculo_id:
            self.mostrar_mensagem("Erro", "Selecione um veículo para apagar.")
            return
        
        # Lógica para apagar o veículo
        # Aqui você pode chamar a lógica de exclusão no banco de dados ou outro processamento
        self.mostrar_mensagem("Veículo Apagado", f"Veículo {veiculo_id} apagado com sucesso!")
        self.atualizar_lista_veiculos()

    def atualizar_lista_veiculos(self):
        """Atualiza a lista de veículos na interface."""
        # Aqui você deve chamar a lógica para obter a lista atualizada de veículos do banco de dados
        # e passar para o método popular_lista.
        veiculos = []  # Substitua isso com a lista real de veículos
        self.popular_lista(veiculos)
