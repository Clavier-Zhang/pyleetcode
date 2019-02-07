import json
class System:

    lang_map = {
        'java': 'java',
        'cpp': 'cpp',
        'python': 'py',
        'python3': 'py',
        'c': 'c',
        'csharp': 'cs',
        'javascript': 'js',
        'ruby': 'rb',
        'swift': 'swift',
        'golang': 'go',
        'scala': 'scala',
        'kotlin': 'kt',
        'rust': 'rs',
        'php': 'php'
    }

    def generate_code_file(self, name, lang, code):
        filename = name + '.' + self.lang_map[lang]
        file = open(filename, 'w')
        file.write(code)
        file.close()