class MKDocsWriter():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.RESPONSE_COLOR = {'200': 'green'}
        self.RESPONSE_NOTATION = {'200': self.success}
        self.ACTION_COLOR = {'get': 'green', 'post': 'orange', 'patch': 'yellow', 'delete': 'red'}

    
    def text(self, text):
        return text + '\n'

    def strong(self, text):
        return  '**' + text + '**' + '\n'
    
    def italics(self, text):
        return '*' + text + '*' + '\n'

    def json_code(self, text):
        return '```json\n'  + text  +'\n' +'```' + '\n'
    
    def code(self, text):
        return '```' + text + '```' + '\n'
    
    def line(self):
        return '****' + '\n'
    
    def heading(self, text, level=1):
        return '#' * level + ' ' + text + '\n'
    
    def table(self, dic, keyname='key', valuename='value'):
        table_string = f'| {keyname} | {valuename} | \n |-|-| \n'
        for key in dic:
            value = dic[key]
            table_string += f'| {key} | {value} | \n'
        
        table_string += '\n'
        return table_string
    
    def text_color(self, text, color='red'):
        return f'<div style="color:{color}">{text}</div>'
    
    def failure(self, text):
        return f'!!! failure \n      {text} \n \n'
    
    def success(self, text):
        return f'!!! success\n      {text} \n \n'