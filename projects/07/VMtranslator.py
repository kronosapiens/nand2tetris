#!/usr/bin/env python
'''
Hack Assembler
Daniel Kronovet
kronovet@gmail.com
'''

COMMENT = '//'

# Create one per input file
class Parser(object):
    def __init__(self, vm_filename):
        self.vm = open(vm_filename, 'r')
        self.next_instruction = None
        self.curr_instruction = None
        self.commands = self.commands_dict()

    #######
    ### API
    def advance(self):
        self.curr_instruction = self.next_instruction
        self.next_instruction = self.load_next_instruction()

    def has_more_commands(self):
        return bool(self.next_instruction)

    @property
    def command_type(self):
        return self.commands.get(self.curr_instruction[0].lower())

    @property
    def arg1(self):
        return self.argn(1)

    @property
    def arg2(self):
        return self.argn(2)

    ### END API
    ###########

    def reset_file(self):
        self.vm.seek(0)
        line = self.vm.readline().strip()
        while not self.is_instruction(line):
            line = self.vm.readline().strip()
        self.load_next_instruction(line)

    def load_next_instruction(self, line=None):
        line = line if line is not None else self.vm.readline().strip()
        self.next_instruction = line.split(COMMENT)[0].strip().split()

    def is_instruction(self, line):
        return line and line[:2] != COMMENT

    def argn(self, n):
        if len(self.curr_instruction) >= n+1
            return self.curr_instruction[n]
        return None

    def commands_dict(self):
        return {
            'add': 'C_ARITHMETIC',
            'sub': 'C_ARITHMETIC',
            'neg': 'C_ARITHMETIC',
             'eq': 'C_ARITHMETIC',
             'gt': 'C_ARITHMETIC',
             'lt': 'C_ARITHMETIC',
            'and': 'C_ARITHMETIC',
             'or': 'C_ARITHMETIC',
            'not': 'C_ARITHMETIC',
           'push': 'C_PUSH',
            'pop': 'C_POP',
          'label': 'C_LABEL',
           'goto': 'C_GOTO',
        'if-goto': 'C_IF',
       'function': 'C_FUNCTION',
         'return': 'C_RETURN',
           'call': 'C_CALL'
        }


class CodeWriter(object):
    def __init__(self, parsers):
        self.parsers = parsers


if __name__ == '__main__':
    import os, sys

    file_path = sys.argv[1]
    parsers = []
    if '.vm' in file_path:
        parsers.append(Parser(file_path))
    else:
        dirname, subdirs, files = os.walk(file_path).next()
        for filename in files:
            if '.vm' in filename:
                parsers.append(Parser(vm_path))