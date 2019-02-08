import json
from .config import lang_dict
from .screen import Screen

class System:

    screen = Screen()

    # helper methods
    def convert_sample_test_case_to_text(self, sample_test_case):
        result = ''
        for line in sample_test_case.splitlines():
            result += ' * '+line+'\n'
        return result

    # code file methods
    def generate_code_file(self, name, lang, code, sample_test_case):
        test_area = ''.join([
            '\n',
            '/**\n',
            ' * Test Area\n',
            ' * This will not be submitted to Leetcode\n',
            ' * Sample Test Case:\n',
            self.convert_sample_test_case_to_text(sample_test_case),
            ' */\n',
        ])
        filename = name + '.' + lang_dict[lang]
        file = open(filename, 'w')
        file.write(code+test_area)
        file.close()
        self.screen.print_generate_code_template_message(filename, lang)

    def get_solution(self, filename):
        raw_codes = open(filename,'r').read()
        solution = ''
        start = False
        for line in raw_codes.splitlines():
            if 'Solution' in line:
                start = True
            if '/**' in line:
                start = False
            if start:
                solution += line+'\n'
        return solution

    def get_test_case(self, filename):
        raw_codes = open(filename,'r').read()
        test_case = ''
        start = False
        for line in raw_codes.splitlines():
            if '*/' in line:
                start = False
            if start:
                line = line.replace(' * ', '')
                test_case += line+'\n'
            if 'Sample Test Case' in line:
                start = True
        return test_case