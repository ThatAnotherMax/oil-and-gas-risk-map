import os
import json


class DataManager(object):
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