TITLES = ['DESCRIPTION', 'PARAMETERS', 'RESPONSE']
SUB_TITLES = ['HEADER', 'PATH', 'BODY']

class Token:
    def __init__(self, token):
        self.OPS = ['+', '-', '/', '*']
        # self.TOKEN_TYPES = ['OP', 'INT', 'VAR', 'PRINT']
        self.value = token
        self.type = self.define_type(token)

    def define_type(self, token):
        if token[1:].upper() in TITLES:
            self.value = token[1:]
            return 'TITLE'
        elif token[:-1].upper() in SUB_TITLES or token[:-1].isdigit():
            self.value = token[:-1]
            return 'SUB'
        elif token == 'EOF':
            return token
        elif token[-1] == '.':
            self.value = token[:-1]
            return 'ENDLINE'
        elif token == '-':
            return 'SEPARATOR'
        elif token == 'file:':
            self.value = 'file'
            return 'FILE'
        else:
            return 'VAR'
