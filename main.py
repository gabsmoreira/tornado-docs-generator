import argparse
import importlib
import json
import re
import sys

from Parser import Parser
from Tokenizer import Tokenizer
from writer import MKDocsWriter

sys.path.append('./lib')


def stripRoute(docstring):
    return docstring.strip()

def getActions(route_class):
    return [method for method in list(route_class.__dict__.keys()) if method in ['get', 'post', 'patch', 'delete']]

def parseFile(file_path):
    splitted = file_path.split('/')
    file = splitted[-1]
    path = '/'.join(splitted[:-1]) + '/'
    if path == '/':
        path = ''
    return file, path

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--filein", help="name of tornado in file", type=str, required=True)
    parser.add_argument("--fileout", help="name of markdown out file", type=str, required=True)
    args = parser.parse_args()

    file, path = parseFile(args.filein)
    sys.path.append(path)
    file_in_no_py = file.split('.py')[0]
    file_out = open(args.fileout, 'w+')
    api = importlib.import_module(file_in_no_py)

    classes = dir(api)
    markdown = MKDocsWriter()
    for class_name_str in classes:
        res = re.search('^[A-Z][a-z]+(?:[A-Z][a-z]+)*$', class_name_str)
        if res is not None:
            file_out.write(markdown.line())
            file_out.write(markdown.heading(markdown.strong(class_name_str), level=2))
            class_name = getattr(api, class_name_str)
            if class_name.__doc__ is not None:
                route = stripRoute(class_name.__doc__)
                file_out.write((markdown.code(route)))
            actions = getActions(class_name)
            for action in actions:
                action = getattr(class_name, action)
                docstring = action.__doc__
                if docstring is not None:
                    docstring = docstring.strip().split(' ')
                    docstring = [d.split('\n')[0] for d in docstring if d != '']
                    color_action_text = markdown.text_color(action.__name__.capitalize(), color=markdown.ACTION_COLOR[action.__name__])
                    file_out.write(markdown.heading(color_action_text, level=3))
                    Parser.run(docstring, file_out, path)
