from Tokenizer import Tokenizer
from writer import MKDocsWriter
import json

class Parser:
    def run(code, file, path):
        Parser.tokens = Tokenizer(code)
        Parser.file = file
        Parser.writer = MKDocsWriter()
        Parser.path = path
        ret = Parser.parseDocstring()
        return ret
    
    def parseDocstring():
        while Parser.tokens.actual.type != 'EOF':
            if Parser.tokens.actual.value == 'Description':
                Parser.parseDescription()
                continue
            
            if Parser.tokens.actual.value == 'Parameters':
                Parser.parseParameters()
                continue
        
            if Parser.tokens.actual.value == 'Response':
                Parser.parseResponse()
                continue
        
            Parser.tokens.select_next()


    def parseParameters():
        parameters = {}
        Parser.tokens.select_next()
        Parser.file.write(Parser.writer.heading('Parameters:', level=4))
        while Parser.tokens.actual.type != 'TITLE':
            if Parser.tokens.actual.value == 'Header':
                Parser.tokens.select_next()
                header = Parser.parseHeader()
                parameters['header'] = header
            if Parser.tokens.actual.value == 'Body':
                Parser.tokens.select_next()
                body = Parser.parseBody()
                parameters['body'] = body
            if Parser.tokens.actual.value == 'Path':
                Parser.tokens.select_next()
                path = Parser.parsePath()
                parameters['path'] = path
            else:
                return parameters
        return parameters
    
    def parsePath():
        path = {}
        Parser.file.write(Parser.writer.heading('Path parameters:', level=5))
        while Parser.tokens.actual.type not in ['EOF', 'TITLE', 'SUB']:
            key = Parser.tokens.actual.value
            Parser.tokens.select_next()
            if Parser.tokens.actual.type != 'SEPARATOR':
                raise SyntaxError(f'Missing - between key and value for path, instead got {Parser.tokens.actual.value}')
            Parser.tokens.select_next()
            value = []
            while Parser.tokens.actual.type != 'ENDLINE':

                value.append(Parser.tokens.actual.value)
                Parser.tokens.select_next()
            value.append(Parser.tokens.actual.value)
            value = ' '.join(value)
            Parser.tokens.select_next()
            path[key] = value

        Parser.file.write(Parser.writer.table(path, keyname='Name', valuename='Description'))
        return path
    
    def parseHeader():
        header = {}
        Parser.file.write(Parser.writer.heading('Header parameters:', level=5))
        while Parser.tokens.actual.type not in ['EOF', 'TITLE', 'SUB']:
            key = Parser.tokens.actual.value
            Parser.tokens.select_next()
            if Parser.tokens.actual.type != 'SEPARATOR':
                raise SyntaxError(f'Missing - between key and value for header, instead got {Parser.tokens.actual.value}')
            Parser.tokens.select_next()
            value = []
            while Parser.tokens.actual.type != 'ENDLINE':
                value.append(Parser.tokens.actual)
                Parser.tokens.select_next()
            value.append(Parser.tokens.actual.value)
            value = ' '.join(value)
            Parser.tokens.select_next()
            header[key] = value
        Parser.file.write(Parser.writer.table(header))
        return header
    
    def parseSchema():
        try:
            with open(Parser.path + Parser.tokens.actual.value) as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f'File from schema {Parser.tokens.actual.value} not found')

    def parseBody():
        body = {}
        Parser.file.write(Parser.writer.heading('Body parameters:', level=5))
        if Parser.tokens.actual.type == 'FILE':
            Parser.tokens.select_next()
            body = Parser.parseSchema()
            body = body['properties']
            Parser.file.write(Parser.writer.json_code(json.dumps(body)))
            return body
        while Parser.tokens.actual.type not in ['EOF', 'TITLE', 'SUB']:
            key = Parser.tokens.actual
            Parser.tokens.select_next()
            if Parser.tokens.actual != '-':
                raise SyntaxError(f'Missing - between key and value for body, instead got {Parser.tokens.actual.value}')
            Parser.tokens.select_next()
            value = []
            while Parser.tokens.actual.type != 'ENDLINE':
                value.append(Parser.tokens.actual)
                Parser.tokens.select_next()
            value.append(Parser.tokens.actual.value)
            value = ' '.join(value)
            Parser.tokens.select_next()
            body[key] = value
        Parser.file.write(Parser.writer.json_code(json.dumps(body)))
        return body
    
    def parseResponse():
        response = {}
        Parser.tokens.select_next()
        Parser.file.write(Parser.writer.heading('Response:', level=4))
        while Parser.tokens.actual.type not in ['EOF', 'TITLE']:
            actual = Parser.tokens.actual.value
            if not actual.isnumeric():
                raise SyntaxError(f'Response must have a code, instead got {Parser.tokens.actual.value}')
            try:
                color = Parser.writer.RESPONSE_COLOR[str(actual)]
            except KeyError:
                color = 'red'
            Parser.file.write(Parser.writer.heading(Parser.writer.text_color(f'Code: {actual}', color=color), level=5))
            key_reponse = str(actual)
            Parser.tokens.select_next()
            if Parser.tokens.actual.type == 'FILE':
                Parser.tokens.select_next()
                body = Parser.parseSchema()
                Parser.tokens.select_next()
                response[key_reponse] = body
                try:
                    color = Parser.writer.RESPONSE_COLOR[str(actual)]
                    Parser.file.write(Parser.writer.RESPONSE_NOTATION[str(actual)](Parser.writer.code(json.dumps(body))))
                except KeyError:
                    Parser.file.write(Parser.writer.failure(Parser.writer.code(json.dumps(body))))
            else:
                body = {}
                while Parser.tokens.actual.type not in ['EOF', 'TITLE', 'SUB']:
                    key = Parser.tokens.actual.value
                    Parser.tokens.select_next()
                    if Parser.tokens.actual.type != 'SEPARATOR':
                        raise SyntaxError(f'Missing - between key and value for reponse, instead got {Parser.tokens.actual.value}')
                    Parser.tokens.select_next()
                    value = []
                    while Parser.tokens.actual.type != 'ENDLINE':
                        value.append(Parser.tokens.actual.value)
                        Parser.tokens.select_next()
                    value.append(Parser.tokens.actual.value)
                    value = ' '.join(value)
                    Parser.tokens.select_next()
                    body[key] = value
                response[key_reponse] = body
                try:
                    color = Parser.writer.RESPONSE_COLOR[str(actual)]
                    Parser.file.write(Parser.writer.RESPONSE_NOTATION[str(actual)](Parser.writer.code(json.dumps(body))))
                except KeyError:
                    Parser.file.write(Parser.writer.failure(Parser.writer.code(json.dumps(body))))
        return response
                    

    
    def parseDescription():
        description = []
        Parser.tokens.select_next()
        Parser.file.write(Parser.writer.heading('Description:', level=4))
        while Parser.tokens.actual.type != 'TITLE':
            description.append(Parser.tokens.actual.value)
            Parser.tokens.select_next()
        description = ' '.join(description)
        Parser.file.write(Parser.writer.text(description))
        return description