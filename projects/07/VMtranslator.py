#!/usr/bin/env python
'''
Hack Assembler
Daniel Kronovet
kronovet@gmail.com
'''

import os

COMMENT = '//'

# Create one per input file
class Parser(object):
    def __init__(self, vm_filename):
        self.vm_filename = vm_filename
        self.vm = open(vm_filename, 'r')
        self.commands = self.commands_dict()
        self.curr_instruction = None
        self.initialize_file()

    #######
    ### API
    def advance(self):
        self.curr_instruction = self.next_instruction
        self.load_next_instruction()

    @property
    def has_more_commands(self):
        return bool(self.next_instruction)

    @property
    def command_type(self):
        return self.commands.get(self.curr_instruction[0].lower())

    @property
    def arg1(self):
        '''Math operation if C_ARITHMETIC'''
        if self.command_type == 'C_ARITHMETIC':
            return self.argn(0)
        return self.argn(1)

    @property
    def arg2(self):
        '''Only return if C_PUSH, C_POP, C_FUNCTION, C_CALL'''
        return self.argn(2)

    ### END API
    ###########

    def initialize_file(self):
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
        if len(self.curr_instruction) >= n+1:
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
    '''Write .asm files

    Contract between methods:
    1. Contents of the A and D registries are not guaranteed,
        so methods must set them to the values they need.
    2. Methods must always leave @SP pointing to the correct location.
    '''
    def __init__(self, asm_filename):
        self.asm = open(asm_filename, 'w')
        self.curr_file = None
        self.bool_count = 0 # Number of boolean comparisons so far

    #######
    ### API
    def set_file_name(self, vm_filename):
        self.curr_file = vm_filename

    def write_arithmetic(self, operation):
        '''Apply operation to top of stack'''
        if operation not in ['neg', 'not']: # Binary operator
            self.pop_to_D()
        self.decrement_SP()
        self.set_A_to_stack()

        if operation == 'add': # Arithmetic operators
            self.write('M=M+D')
        elif operation == 'sub':
            self.write('M=M-D')
        elif operation == 'and':
            self.write('M=M&D')
        elif operation == 'or':
            self.write('M=M|D')
        elif operation == 'neg':
            self.write('M=-M')
        elif operation == 'not':
            self.write('M=!M')
        elif operation in ['eq', 'gt', 'lt']: # Boolean operators
            self.write('D=M-D')
            self.write('@BOOL{}'.format(self.bool_count))

            if operation == 'eq':
                self.write('D;JEQ') # if x == y, x - y == 0
            elif operation == 'gt':
                self.write('D;JGT') # if x > y, x - y > 0
            elif operation == 'lt':
                self.write('D;JLT') # if x < y, x - y < 0

            self.set_A_to_stack()
            self.write('M=0') # False
            self.write('@ENDBOOL{}'.format(self.bool_count))
            self.write('0;JMP')

            self.write('(BOOL{})'.format(self.bool_count))
            self.set_A_to_stack()
            self.write('M=-1') # True

            self.write('(ENDBOOL{})'.format(self.bool_count))
            self.bool_count += 1
        else:
            self.raise_unknown(operation)
        self.increment_SP()

    def write_push_pop(self, command, segment, index):
        if command == 'C_PUSH':
            self.load_address(segment, index)
            self.push_from_D()
        elif command == 'C_POP':
            self.pop_to_D()
            self.write('M=D')
        else:
            self.raise_unknown(command)

    def close(self):
        self.asm.close()

    ### END API
    ###########
    def write(self, command):
        self.asm.write(command + '\n')

    def raise_unknown(self, command):
        raise ValueError('{} is an invalid command'.format(command))

    def load_address(self, segment, index):
        '''Resolve segment + index to address, load M[address] to D'''
        if segment == 'constant':
            self.write('@{}'.format(index))
            self.write('D=A')
        else:
            # Resolve address
            self.write('D=M')

    def save_address(self, segment, index):
        '''Resolve segment + index to address, load D to M[address]'''
        pass

    def resolve_address(self, segment, index):
        pass

    def push_from_D(self):
        '''Push from D onto top of stack, increment @SP'''
        self.write('@SP') # Get current stack pointer
        self.write('A=M') # Set address to current stack pointer
        self.write('M=D') # Write data to top of stack
        self.write('@SP') # Increment SP
        self.write('M=M+1')

    def pop_to_D(self):
        '''Decrement @SP, pop from top of stack onto D'''
        self.write('@SP')
        self.write('M=M-1') # Decrement SP
        self.write('A=M') # Set address to current stack pointer
        self.write('D=M') # Get data from top of stack

    def decrement_SP(self):
        self.write('@SP')
        self.write('M=M-1')

    def increment_SP(self):
        self.write('@SP')
        self.write('M=M+1')

    def set_A_to_stack(self):
        self.write('@SP')
        self.write('A=M')


class Main(object):
    def __init__(self, file_path):
        self.parse_files(file_path)
        self.cw = CodeWriter(self.asm_file)
        for vm_file in self.vm_files:
            self.translate(vm_file)

    def parse_files(self, file_path):
        if '.vm' in file_path:
            self.asm_file = file_path.replace('.vm', '.asm')
            self.vm_files = [file_path]
        else:
            file_path = file_path[:-1] if file_path[-1] == '/' else file_path
            path_elements = file_path.split('/')
            path = '/'.join(path_elements)
            self.asm_file = path + '/' + path_elements[-1] + '.asm'
            dirpath, dirnames, filenames = next(os.walk(file_path), [[],[],[]])
            vm_files = filter(lambda x: '.vm' in x, filenames)
            self.vm_files = [path + '/' +  vm_file for vm_file in vm_files]

    def translate(self, vm_file):
        parser = Parser(vm_file)
        self.cw.set_file_name(vm_file)
        while parser.has_more_commands:
            parser.advance()
            if parser.command_type == 'C_PUSH':
                self.cw.write_push_pop('C_PUSH', parser.arg1, parser.arg2)
            elif parser.command_type == 'C_POP':
                self.cw.write_push_pop('C_POP', parser.arg1, parser.arg2)
            elif parser.command_type == 'C_ARITHMETIC':
                self.cw.write_arithmetic(parser.arg1)


if __name__ == '__main__':
    import sys

    file_path = sys.argv[1]
    Main(file_path)