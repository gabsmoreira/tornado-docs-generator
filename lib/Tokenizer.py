from Token import Token
class Tokenizer:
    def __init__(self, doc):
        self.docstring = doc
        self.index = 0
        self.actual = Token(self.docstring[self.index])

    def select_next(self):
        index = self.index
        has_blank = False
        if(self.index == len(self.docstring)):
            self.actual = Token('EOF')
            return 
        while self.docstring[index] in [' ', ''] and (index == len(self.docstring)):
            has_blank = True
            index += 1
        self.index = index if has_blank else index + 1
        if(self.index == len(self.docstring)):
            self.actual = Token('EOF')
            return   
        self.actual = Token(self.docstring[self.index])
        
