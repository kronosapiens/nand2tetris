#!/usr/bin/env python
'''
Jack Analyzer
Daniel Kronovet
kronovet@gmail.com
'''

import os
from collections import deque


class JackAnalyzer(object):
    def __init__(self, file_path):
        jack_files = self.parse_files(file_path)
        for jack_file in jack_files:
            self.analyze(jack_file)

    def parse_files(self, file_path):
        if '.jack' in file_path:
            return [file_path]
        else:
            file_path = file_path[:-1] if file_path[-1] == '/' else file_path
            # path_elements = file_path.split('/')
            # path = '/'.join(path_elements)
            dirpath, dirnames, filenames = next(os.walk(file_path), [[],[],[]])
            jack_files = filter(lambda x: '.jack' in x, filenames)
            return [file_path + '/' +  jack_file for jack_file in jack_files]

    def analyze(self, jack_file):
        tokenizer = JackTokenizer(jack_file)
        ce = CompilationEngine(jack_file)
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            if tokenizer.token_type == 'KEYWORD':

                ce.write_token('keyword', tokenizer.curr_token)
            elif tokenizer.token_type == 'SYMBOL':
                ce.write_token('symbol', tokenizer.curr_token)
            elif tokenizer.token_type == 'INT_CONSTANT':
                ce.write_token('integerConstant', str(tokenizer.curr_token))
            elif tokenizer.token_type == 'STRING_CONSTANT':
                ce.write_token('stringConstant', tokenizer.curr_token)
            elif tokenizer.token_type == 'IDENTIFIER':
                ce.write_token('identifier', tokenizer.curr_token)
        ce.close()

class JackTokenizer(object):
    #######
    ### API
    def __init__(self, jack_filename):
        self.jack_filename = jack_filename
        self.jack = self.load_file(self.jack_filename)
        self.curr_token = None
        self.token_type = None
        self.keywords = self.keyword_dict()
        self.symbols = self.symbol_set()

    def has_more_tokens(self):
        return self.jack

    def advance(self):
        next_token = self.jack.popleft()

        # Symbol
        if next_token[0] in self.symbols:
            self.token_type = 'SYMBOL'
            if len(next_token) >= 2 and next_token[:2] in ['++', '<=', '>=']:
                self.curr_token = next_token[:2]
                if next_token[2:]:
                    self.jack.appendleft(next_token[2:])
            else:
                self.curr_token = next_token[0]
                if next_token[1:]:
                    self.jack.appendleft(next_token[1:])
            return

        # String Constant
        if next_token[0] == '"':
            self.token_type = 'STRING_CONSTANT'
            curr_string = next_token[1:]
            full_string = ''
            while True:
                for i, el in enumerate(curr_string):
                    if el == '"':
                        full_string += curr_string[:i]
                        if curr_string[i+1:]:
                            self.jack.appendleft(curr_string[i+1:])
                        self.curr_token = full_string.strip()
                        return
                full_string += curr_string + ' '
                curr_string = self.jack.popleft()

        # Integer Constant
        if self.is_int(next_token[0]):
            self.token_type = 'INT_CONSTANT'
            int_idx = 0
            while self.is_int(next_token[:int_idx+1]):
                int_idx += 1
            self.curr_token = next_token[:int_idx]
            if next_token[int_idx:]:
                self.jack.appendleft(next_token[int_idx:])
            return

        # Identifier or Keyword
        # Need to check for trailing symbol
        self.curr_token = next_token
        for i, el in enumerate(next_token):
            if el in self.symbols:
                self.curr_token = next_token[:i]
                self.jack.appendleft(next_token[i:])
                break
        if self.curr_token in self.keywords:
            self.token_type = 'KEYWORD'
        else:
            self.token_type = 'IDENTIFIER'

    def token_type(self):
        return self.token_type

    def key_word(self):
        return self.keywords[self.curr_token]

    def symbol(self):
        return self.curr_token

    def identifier(self):
        return self.curr_token

    def int_val(self):
        return int(self.curr_token)

    def string_val(self):
        return self.curr_token

    ### END API
    ###########

    def load_file(self, jack_filename):
        with open(jack_filename, 'r') as f:
            contents = f.read()
        contents = contents.split('\n')
        contents = [l.strip() for l in contents]
        contents = [l.split('//')[0] for l in contents]
        in_comment = False
        for i, line in enumerate(contents):
            start, end = line[:2], line[-2:]
            if start == '/*':
                in_comment = True

            if in_comment:
                contents[i] = ''

            if start == '*/' or end == '*/':
                in_comment = False
        words = []
        for line in contents:
            words.extend(line.split())
        words = [l for l in words if l]
        return deque(words)

    def is_int(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def keyword_dict(self):
        return {
            'class': 'CLASS',
            'constructor': 'CONSTRUCTOR',
            'function': 'FUNCTION',
            'method': 'METHOD',
            'field': 'FIELD',
            'static': 'STATIC',
            'var': 'VAR',
            'int': 'INT',
            'char': 'CHAR',
            'boolean': 'BOOLEAN',
            'void': 'VOID',
            'true': 'TRUE',
            'false': 'FALSE',
            'null': 'NULL',
            'this': 'THIS',
            'let': 'LET',
            'do': 'DO',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'return': 'RETURN'
        }

    def symbol_set(self):
        return set([
            '{',
            '}',
            '(',
            ')',
            '[',
            ']',
            '.',
            ',',
            ';',
            '+',
            '-',
            '*',
            '/',
            '&',
            '|',
            '<',
            '>',
            '=',
            '~',
        ])



class CompilationEngine(object):
    #######
    ### API
    def __init__(self, jack_filename):
        filename_pieces = jack_filename.split('/')
        filename_pieces[-1] = 'My' + filename_pieces[-1] # Avoid overwriting original file
        xml_filename = '/'.join(filename_pieces).replace('.jack', '.xml')
        self.xml = open(xml_filename, 'w')
        self.indent = 0
        self.write('<tokens>\n')
        self.updent()

    def compile_class(self):

        pass

    def compile_class_var_dec(self):
        pass

    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass

    ### END API
    ###########

    def write(self, content):
        self.xml.write(content)

    def write_token(self, token_type, token):
        token = token.replace('&', '&amp;')
        token = token.replace('<', '&lt;')
        token = token.replace('>', '&gt;')
        self.write(' ' * self.indent + '<' + token_type.lower() + '> ')
        self.write(token)
        self.write(' </' + token_type.lower() + '>\n')

    def close(self):
        self.downdent()
        self.write('</tokens>')
        self.xml.close()

    def updent(self):
        self.indent += 2

    def downdent(self):
        self.indent -= 2


if __name__ == '__main__':
    import sys

    file_path = sys.argv[1]
    JackAnalyzer(file_path)