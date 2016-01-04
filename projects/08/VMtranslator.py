#!/usr/bin/env python
'''
VM Translator
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
        self.EOF = False
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
        return not self.EOF

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
    def close(self):
        self.vm.close()

    def initialize_file(self):
        self.vm.seek(0)
        self.load_next_instruction()

    def load_next_instruction(self, line=None):
        loaded = False
        while not loaded and not self.EOF:
            tell = self.vm.tell()
            line = self.vm.readline().strip()
            if self.is_instruction(line):
                self.next_instruction = line.split(COMMENT)[0].strip().split()
                loaded = True
            if tell == self.vm.tell(): # File position did not change
                self.EOF = True

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
        self.addresses = self.address_dict()
        self.line_count = 0
        self.bool_count = 0 # Number of boolean comparisons so far
        self.call_count = 0 # Number of function calls so far

    #######
    ### API
    def write_init(self):
        self.write('@256')
        self.write('D=A')
        self.write('@SP')
        self.write('M=D')
        self.write_call('Sys.init', 0)
        # self.write('@Sys.init')
        # self.write('0;JMP')

    def set_file_name(self, vm_filename):
        '''Reset pointers'''
        self.curr_file = vm_filename.replace('.vm', '').split('/')[-1]
        # self.curr_file = vm_filename.replace('.vm', '')
        self.write('//////', code=False)
        self.write('// {}'.format(self.curr_file), code=False)

    def write_arithmetic(self, operation):
        '''Apply operation to top of stack'''
        if operation not in ['neg', 'not']: # Binary operator
            self.pop_stack_to_D()
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

            self.write('(BOOL{})'.format(self.bool_count), code=False)
            self.set_A_to_stack()
            self.write('M=-1') # True

            self.write('(ENDBOOL{})'.format(self.bool_count), code=False)
            self.bool_count += 1
        else:
            self.raise_unknown(operation)
        self.increment_SP()

    def write_push_pop(self, command, segment, index):
        self.resolve_address(segment, index)
        if command == 'C_PUSH': # load M[address] to D
            if segment == 'constant':
                self.write('D=A')
            else:
                self.write('D=M')
            self.push_D_to_stack()
        elif command == 'C_POP': # load D to M[address]
            self.write('D=A')
            self.write('@R13') # Store resolved address in R13
            self.write('M=D')
            self.pop_stack_to_D()
            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        else:
            self.raise_unknown(command)

    def write_label(self, label):
        self.write('({}${})'.format(self.curr_file, label), code=False)

    def write_goto(self, label):
        self.write('@{}${}'.format(self.curr_file, label))
        self.write('0;JMP')

    def write_if(self, label):
        self.pop_stack_to_D()
        self.write('@{}${}'.format(self.curr_file, label))
        self.write('D;JNE')

    def write_function(self, function_name, num_locals):
        # (f)
        self.write('({})'.format(function_name), code=False)

        # k times: push 0
        for _ in xrange(num_locals): # Initialize local vars to 0
            self.write('D=0')
            self.push_D_to_stack()

    def write_call(self, function_name, num_args):
        RET = function_name + 'RET' +  str(self.call_count) # Unique return label
        self.call_count += 1

        # push return-address
        self.write('@' + RET)
        self.write('D=A')
        self.push_D_to_stack()

        # push LCL
        # push ARG
        # push THIS
        # push THAT
        for address in ['@LCL', '@ARG', '@THIS', '@THAT']:
            self.write(address)
            self.write('D=M')
            self.push_D_to_stack()

        # LCL = SP
        self.write('@SP')
        self.write('D=M')
        self.write('@LCL')
        self.write('M=D')

        # ARG = SP-n-5
        # self.write('@SP') # Redundant b/c of prev two commands
        # self.write('D=M') # Redundant b/c of prev two commands
        self.write('@' + str(num_args + 5))
        self.write('D=D-A')
        self.write('@ARG')
        self.write('M=D')

        # goto f
        self.write('@' + function_name)
        self.write('0;JMP')

        # (return_address)
        self.write('({})'.format(RET), code=False)

    def write_return(self):
        # Temporary variables
        FRAME = 'R13'
        RET = 'R14'

        # FRAME = LCL
        self.write('@LCL')
        self.write('D=M')
        self.write('@' + FRAME)
        self.write('M=D')

        # RET = *(FRAME-5)
        # Can't be included in iterator b/c value will be overwritten if num_args=0
        self.write('@' + FRAME)
        self.write('D=M') # Save start of frame
        self.write('@5')
        self.write('D=D-A') # Adjust address
        self.write('A=D') # Prepare to load value at address
        self.write('D=M') # Store value
        self.write('@' + RET)
        self.write('M=D') # Save value

        # *ARG = pop()
        self.pop_stack_to_D()
        self.write('@ARG')
        self.write('A=M')
        self.write('M=D')

        # SP = ARG+1
        self.write('@ARG')
        self.write('D=M')
        self.write('@SP')
        self.write('M=D+1')

        # THAT = *(FRAME-1)
        # THIS = *(FRAME-2)
        # ARG = *(FRAME-3)
        # LCL = *(FRAME-4)
        offset = 1
        for address in ['@THAT', '@THIS', '@ARG', '@LCL']:
            self.write('@' + FRAME)
            self.write('D=M') # Save start of frame
            self.write('@' + str(offset))
            self.write('D=D-A') # Adjust address
            self.write('A=D') # Prepare to load value at address
            self.write('D=M') # Store value
            self.write(address)
            self.write('M=D') # Save value
            offset += 1

        # goto RET
        self.write('@' + RET)
        self.write('A=M')
        self.write('0;JMP')

    ### END API
    ###########
    def write(self, command, code=True):
        self.asm.write(command)
        if code:
            self.asm.write(' // ' + str(self.line_count))
            self.line_count += 1
        self.asm.write('\n')

    def close(self):
        self.asm.close()

    def raise_unknown(self, argument):
        raise ValueError('{} is an invalid argument'.format(argument))

    def resolve_address(self, segment, index):
        '''Resolve address to A register'''
        address = self.addresses.get(segment)
        if segment == 'constant':
            self.write('@' + str(index))
        elif segment == 'static':
            self.write('@' + self.curr_file + '.' + str(index))
        elif segment in ['pointer', 'temp']:
            self.write('@R' + str(address + index)) # Address is an int
        elif segment in ['local', 'argument', 'this', 'that']:
            self.write('@' + address) # Address is a string
            self.write('D=M')
            self.write('@' + str(index))
            self.write('A=D+A') # D is segment base
        else:
            self.raise_unknown(segment)

    def address_dict(self):
        return {
            'local': 'LCL', # Base R1
            'argument': 'ARG', # Base R2
            'this': 'THIS', # Base R3
            'that': 'THAT', # Base R4
            'pointer': 3, # Edit R3, R4
            'temp': 5, # Edit R5-12
            # R13-15 are free
            'static': 16, # Edit R16-255
        }

    def push_D_to_stack(self):
        '''Push from D onto top of stack, increment @SP'''
        self.write('@SP') # Get current stack pointer
        self.write('A=M') # Set address to current stack pointer
        self.write('M=D') # Write data to top of stack
        self.increment_SP()

    def pop_stack_to_D(self):
        '''Decrement @SP, pop from top of stack onto D'''
        self.decrement_SP()
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
        self.cw.write_init()
        for vm_file in self.vm_files:
            self.translate(vm_file)
        self.cw.close()

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
            self.cw.write('// ' + ' '.join(parser.curr_instruction), code=False)
            if parser.command_type == 'C_PUSH':
                self.cw.write_push_pop('C_PUSH', parser.arg1, int(parser.arg2))
            elif parser.command_type == 'C_POP':
                self.cw.write_push_pop('C_POP', parser.arg1, int(parser.arg2))
            elif parser.command_type == 'C_ARITHMETIC':
                self.cw.write_arithmetic(parser.arg1)
            elif parser.command_type == 'C_LABEL':
                self.cw.write_label(parser.arg1)
            elif parser.command_type == 'C_GOTO':
                self.cw.write_goto(parser.arg1)
            elif parser.command_type == 'C_IF':
                self.cw.write_if(parser.arg1)
            elif parser.command_type == 'C_FUNCTION':
                self.cw.write_function(parser.arg1, int(parser.arg2))
            elif parser.command_type == 'C_CALL':
                self.cw.write_call(parser.arg1, int(parser.arg2))
            elif parser.command_type == 'C_RETURN':
                self.cw.write_return()
        parser.close()


if __name__ == '__main__':
    import sys

    file_path = sys.argv[1]
    Main(file_path)