import json
from .config import lang_dict

class System:

    def generate_code_file(self, name, lang, code):
        filename = name + '.' + lang_dict[lang]
        file = open(filename, 'w')
        file.write(code)
        file.close()