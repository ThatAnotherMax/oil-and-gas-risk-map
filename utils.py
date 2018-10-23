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


class AccidentManager(object):
    s_accidents = {
        "gas": [
            {
                "ID": "a1",
                "Name": "Аварія 1",
                "Model": Accident1
            },
            {
                "ID": "a2",
                "Name": "Аварія 2",
                "Model": Accident2
            },
        ]
    }

    @staticmethod
    def getAccidents(category):
        if category not in AccidentManager.s_accidents:
            return None

        return AccidentManager.s_accidents[category]

    @staticmethod
    def getAccidentsDescriptions(category):
        accidents = AccidentManager.getAccidents(category)
        descriptions = []

        for accident in accidents:
            description = {
                "ID": accident.get("ID"),
                "Name": accident.get("Name")
            }

            descriptions.append(description)

        return descriptions


