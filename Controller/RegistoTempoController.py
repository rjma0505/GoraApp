# Controller/RegistoTempoController.py

from View.RegistoTempoView import RegistoTempoView
from DAO.RegistoTempoDAO import RegistoTempoDAO

class RegistoTempoController:
    def __init__(self, folha_servico_id):
        self.folha_servico_id = folha_servico_id
        self.view = RegistoTempoView()
        self.dao = RegistoTempoDAO()

    def iniciar(self):
        """Abre a view e carrega os registos de tempo da folha"""
        registos = self.dao.obter_registos_por_folha(self.folha_servico_id)
        self.view.popular_tabela(registos)
        self.view.exec_()
