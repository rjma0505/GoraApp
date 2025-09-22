# View/CriarOrcamentoDialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from DAO.ClienteDAO import ClienteDAO
from DAO.VeiculoDAO import VeiculoDAO
from Model.Orcamento import Orcamento

class CriarOrcamentoDialog(QDialog):
    def __init__(self, controller, orcamento_id=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.orcamento_id = orcamento_id
        self.setWindowTitle("Criar / Editar Orçamento")
        self.resize(500, 400)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Combobox de clientes
        self.cliente_combo = QComboBox()
        self.clientes = ClienteDAO().listar_clientes()
        for c in self.clientes:
            self.cliente_combo.addItem(c['nome'], c['id'])
        form_layout.addRow("Cliente:", self.cliente_combo)

        # Combobox de veículos
        self.veiculo_combo = QComboBox()
        self.veiculos = []
        if self.clientes:
            primeiro_cliente_id = self.clientes[0]['id']
            self.carregar_veiculos(primeiro_cliente_id)
        form_layout.addRow("Veículo:", self.veiculo_combo)

        # Atualizar veículos quando mudar cliente
        self.cliente_combo.currentIndexChanged.connect(self.on_cliente_change)

        # Campos de descrição, valor e validade
        self.descricao_input = QLineEdit()
        self.valor_input = QLineEdit()
        self.validade_input = QLineEdit()
        form_layout.addRow("Descrição:", self.descricao_input)
        form_layout.addRow("Valor Estimado:", self.valor_input)
        form_layout.addRow("Validade (YYYY-MM-DD):", self.validade_input)

        # Combobox de estado
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["pendente", "aprovado", "rejeitado"])
        form_layout.addRow("Estado:", self.estado_combo)

        layout.addLayout(form_layout)

        # Botões Guardar / Cancelar
        self.btn_guardar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_cancelar)

        self.setLayout(layout)

        # Conectar sinais
        self.btn_guardar.clicked.connect(self.guardar_orcamento)
        self.btn_cancelar.clicked.connect(self.close)

        # Se for edição, carregar dados
        if self.orcamento_id:
            self._carregar_orcamento()

    def carregar_veiculos(self, cliente_id):
        self.veiculo_combo.clear()
        self.veiculos = VeiculoDAO().listar_veiculos_por_cliente(cliente_id)
        for v in self.veiculos:
            display = f"{v.marca} {v.modelo} ({v.matricula})"
            self.veiculo_combo.addItem(display, v.id)

    def on_cliente_change(self, index):
        cliente_id = self.cliente_combo.itemData(index)
        self.carregar_veiculos(cliente_id)

    def _carregar_orcamento(self):
        """Carrega os dados de um orçamento existente para edição"""
        resultados = self.controller.dao.listar_todos_orcamentos()
        
        # Converter dicts em objetos Orcamento
        orcamentos = []
        for r in resultados:
            o = Orcamento(
                cliente_id=r['cliente_id'],
                veiculo_id=r['veiculo_id'],
                descricao=r['descricao'],
                valor_estimado=r['valor_estimado'],
                validade=r['validade'],
                estado=r['estado'],
                id=r['id'],
                data_criacao=r.get('data_criacao')
            )
            o.cliente_nome = r.get('cliente_nome')
            o.veiculo_marca = r.get('veiculo_marca')
            o.veiculo_modelo = r.get('veiculo_modelo')
            orcamentos.append(o)
        
        orcamento = next((o for o in orcamentos if o.id == self.orcamento_id), None)
        if not orcamento:
            QMessageBox.warning(self, "Erro", "Orçamento não encontrado.")
            self.close()
            return

        # Selecionar cliente
        idx_cliente = self.cliente_combo.findData(orcamento.cliente_id)
        if idx_cliente >= 0:
            self.cliente_combo.setCurrentIndex(idx_cliente)

        # Atualizar veículos e selecionar veículo
        self.carregar_veiculos(orcamento.cliente_id)
        idx_veiculo = self.veiculo_combo.findData(orcamento.veiculo_id)
        if idx_veiculo >= 0:
            self.veiculo_combo.setCurrentIndex(idx_veiculo)

        self.descricao_input.setText(orcamento.descricao)
        self.valor_input.setText(str(orcamento.valor_estimado))
        self.validade_input.setText(str(orcamento.validade))

        idx_estado = self.estado_combo.findText(orcamento.estado)
        if idx_estado >= 0:
            self.estado_combo.setCurrentIndex(idx_estado)

    def guardar_orcamento(self):
        try:
            cliente_id = self.cliente_combo.currentData()
            veiculo_id = self.veiculo_combo.currentData()
            descricao = self.descricao_input.text()
            valor = float(self.valor_input.text())
            validade = self.validade_input.text()
            estado = self.estado_combo.currentText()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Dados inválidos: {e}")
            return

        if self.orcamento_id:
            # Atualizar orçamento existente
            orcamento = Orcamento(cliente_id, veiculo_id, descricao, valor, validade, estado, id=self.orcamento_id)
            self.controller.editar_orcamento(orcamento)
        else:
            # Criar novo orçamento
            self.controller.criar_orcamento(cliente_id, veiculo_id, descricao, valor, validade, estado)

        self.close()
