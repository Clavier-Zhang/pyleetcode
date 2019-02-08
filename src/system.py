import json
from .config import lang_dict
from .screen import Screen
class System:

    screen = Screen()

    def generate_code_file(self, name, lang, code):
        filename = name + '.' + lang_dict[lang]
        file = open(filename, 'w')
        file.write(code)
        file.close()
        self.screen.print_generate_code_template_message(filename, lang)
