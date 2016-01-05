#!/usr/bin/env python
'''
Jack Analyzer
Daniel Kronovet
kronovet@gmail.com
'''

import os


class JackAnalyzer(object):
    def __init__(self):
        pass


class JackTokenizer(object):
    #######
    ### API
    def __init__(self):
        pass

    def has_more_tokens(self):
        pass

    def advance(self):
        pass

    def token_type(self):
        pass

    def key_word(self):
        pass

    def symbol(self):
        pass

    def identifier(self):
        pass

    def int_val(self):
        pass

    def string_val(self):
        pass

    ### END API
    ###########


class CompilationEngine(object):
    #######
    ### API
    def __init__(self):
        pass

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


if __name__ == '__main__':
    import sys

    file_path = sys.argv[1]
    Main(file_path)