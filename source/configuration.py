import json
import os


class Configuration:
    common = {}
    APPLICATION_ROOT = None

    @staticmethod
    def get_hs_configuration(filename):
        syntax_file_fullpath = os.path.join(Configuration.APPLICATION_ROOT, 'config', filename)
        #print(syntax_file_fullpath)
        with open(syntax_file_fullpath) as json_file:
            hs_data = json.load(json_file)
        return hs_data
