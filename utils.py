import os
import json

from app import app
from models import Accident1, Accident2


class DataManager(object):
    s_categories  = {
        "gas": "Газопровод",
        "oil": "Нафтопровод",
    }

    @staticmethod
    def root_dir():  # pragma: no cover
        return os.path.abspath(os.path.dirname(__file__))

    @staticmethod
    def get_file(filename):
        try:
            src = os.path.join(DataManager.root_dir(), filename)
            # Figure out how flask returns static files
            # Tried:
            # - render_template
            # - send_file
            # This should not be so non-obvious
            return open(src).read()
        except IOError as exc:
            return str(exc)

    @staticmethod
    def read_data(file_path):
        complete_path = os.path.join(DataManager.root_dir(), file_path)

        json_data = DataManager.get_file(complete_path)

        data = json.loads(json_data)

        return data

    @staticmethod
    def write_data(file_path, data):
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    @staticmethod
    def getCategories():
        return DataManager.s_categories

    @staticmethod
    def getCategoryData(category):
        if category is None:
            return None        

        if category not in DataManager.s_categories:
            return None

        category_data_fpath = {
            "oil": os.path.join(app.config['DATA_FOLDER'], app.config['OIL_DATA_FILE']),
            "gas": os.path.join(app.config['DATA_FOLDER'], app.config['GAS_DATA_FILE']),
        }

        return DataManager.read_data(category_data_fpath.get(category))

class Model(object):
    def params(self, params):
        self._onParams(params)

    def _onParams(self, params):
        pass

    def process(self):
        return self._onProcess()

class ModelCollectiveRisk(Model):
    def __init__(self):
        self.square = 0
        self.h = 0
        self.phi_min = 0
        self.phi_max = 0
        self.f_x_y_phi = None
        self.psi = None

    def _onParams(self, params):
        self.square = float(params.get("square"))
        self.h = int(params.get("h"))
        self.phi_min = int(params.get("phi_min"))
        self.phi_max = int(params.get("phi_max"))
        self.f_x_y_phi = params.get("f_x_y_phi")
        self.psi = params.get("psi")

    def _onProcess(self):

        return self.h * self.phi_min * self.square


class ModelManager(object):
    s_models = {}

    @staticmethod
    def addModel(model_name, model_type):
        if model_name and model_type:
            model = model_type()
            ModelManager.s_models[model_name] = model

    @staticmethod
    def hasModel(model_name):
        return model_name in ModelManager.s_models

    @staticmethod
    def getModel(model_name):
        if ModelManager.hasModel(model_name):
            return ModelManager.s_models[model_name]

# dummy model register
ModelManager.addModel("collective-risk", ModelCollectiveRisk)
