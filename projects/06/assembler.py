#!/usr/bin/env python
'''
Hack Assembler
Daniel Kronovet
kronovet@gmail.com

This implementation sticks closely to the API defined by the authors.
That said, I'm not thrilled with this implementation. The API given by the
authors felt a bit heavy; if time permits it would be worth reimplementing
this with a thinner interface, specifically by minimizing the SymbolTable API
and integrating Assembler and Parser into a single object.
'''


class Assembler(object):
    def __init__(self, parser, symbol_table, code):
        self.parser = parser
        self.symbol_table = symbol_table
        self.code = code

    def assemble(self, asm_filename):
        self.prepare_files(asm_filename)
        parser = self.parser

        # First pass to build label table
        while parser.has_more_commands:
            parser.advance()
            if parser.command_type == 'L_COMMAND':
                self.write_L(parser.symbol)

        # Second pass to write .hack file
        parser.reset_file()
        self.ram_address = 16
        while parser.has_more_commands:
            parser.advance()
            if parser.command_type == 'A_COMMAND':
                self.write_A(parser.symbol)
            elif parser.command_type == 'C_COMMAND':
                self.write_C(parser.dest, parser.comp, parser.jump)

        parser.close_asm()
        self.hack.close()

    def prepare_files(self, asm_filename):
        assert '.asm' in asm_filename, 'Must pass .asm file!'
        self.parser.load_file(asm_filename)
        hack_filename = asm_filename.replace('.asm', '.hack')
        self.hack = open(hack_filename, 'w')

    def create_address(self, symbol):
        address = '{0:b}'.format(int(symbol))
        base = (15 - len(address)) * '0'
        return base + address

    def write(self, instruction):
        self.hack.write(instruction + '\n')

    def write_A(self, symbol):
        instruction = '0'
        try:
            int(symbol)
        except ValueError:
            if not self.symbol_table.contains(symbol): # Build table on first pass
                address = self.create_address(self.ram_address)
                self.symbol_table.add_entry(symbol, address)
                self.ram_address += 1
            instruction += self.symbol_table.get_address(symbol)
        else:
            instruction += self.create_address(symbol)

        self.write(instruction)

    def write_L(self, symbol):
        address = self.create_address(self.parser.instruction_num+1)
        self.symbol_table.add_entry(symbol, address)

    def write_C(self, dest, comp, jump):
        instruction = '111'
        instruction += self.code.comp(comp)
        instruction += self.code.dest(dest)
        instruction += self.code.jump(jump)
        self.write(instruction)

class Parser(object):
    def load_file(self, asm_filename):
        self.asm = open(asm_filename, 'r')
        self.reset_file()
        self.symbol = None
        self.dest = None
        self.comp = None
        self.jump = None
        self.command_type = None

    def reset_file(self):
        self.asm.seek(0)
        line = self.asm.readline().strip()
        while self.is_not_instruction(line):
            line = self.asm.readline().strip()
        self.curr_instruction = line
        self.instruction_num = -1 # 0 once first instruction is parsed.

    def close_asm(self):
        self.asm.close()

    def is_not_instruction(self, line):
        return not line or line[:2] == '//'

    @property
    def has_more_commands(self):
        return bool(self.curr_instruction)

    def get_next_instruction(self):
        line = self.asm.readline().strip()
        line = line.split('//')[0]
        line = line.strip()
        self.curr_instruction = line

    def advance(self):
        '''Parse current instruction and load next instruction
        '''
        ci = self.curr_instruction
        if ci[0] == '@':
            self.parse_A(ci)
            self.instruction_num += 1
        elif ci[0] == '(':
            self.parse_L(ci)
        else:
            self.parse_C(ci)
            self.instruction_num += 1
        self.get_next_instruction()

    def parse_A(self, instruction):
        '''A instruction format: @address
        '''
        self.symbol = instruction[1:]
        self.command_type = 'A_COMMAND'

    def parse_L(self, instruction):
        '''L instruction format: (LABEL)
        '''
        self.symbol = instruction[1:-1]
        self.command_type = 'L_COMMAND'

    def parse_C(self, instruction):
        '''C instruction format: dest=comp;jump
        '''
        self.dest, self.comp, self.jump = None, None, None
        parts = instruction.split(';')
        remainder = parts[0]
        if len(parts) == 2:
            self.jump = parts[1]
        parts = remainder.split('=')
        if len(parts) == 2:
            self.dest = parts[0]
            self.comp = parts[1]
        else:
            self.comp = parts[0]
        self.command_type = 'C_COMMAND'


class Code(object):
    def dest(self, mnemonic):
        '''Alt: Enumerate all possibilities and do dictionary lookup.
        Current implemention is more flexible,
            but slower (max 9 comparisons vs 1 hashing)
        '''
        bin = ['0', '0', '0']
        if mnemonic is None:
            return ''.join(bin)
        if 'A' in mnemonic:
            bin[0] = '1'
        if 'D' in mnemonic:
            bin[1] = '1'
        if 'M' in mnemonic:
            bin[2] = '1'
        return ''.join(bin)

    def comp(self, mnemonic):
        comp_dict = {
              '0': '101010',
              '1': '111111',
             '-1': '111010',
              'D': '001100',
              'A': '110000',
             '!D': '001101',
             '!A': '110001',
             '-D': '001111',
             '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101',
        }
        a_bit = '0'
        if 'M' in mnemonic:
            a_bit = '1'
            mnemonic = mnemonic.replace('M', 'A')
        c_bit = comp_dict.get(mnemonic, '000000')
        return a_bit + c_bit

    def jump(self, mnemonic):
        jump_dict = {
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }
        return jump_dict.get(mnemonic, '000')


class SymbolTable(object):
    def __init__(self):
        self.symbol_dict = self.base_table()
        self.ram_position = 16 # 0-15 have preset values

    def get_address(self, symbol):
        return self.symbol_dict[symbol]

    def contains(self, symbol):
        return symbol in self.symbol_dict

    def add_entry(self, symbol, address):
        self.symbol_dict[symbol] = address

    def base_table(self): # 15 bit addresses, 32K locations
        return {
             'SP': '000000000000000',
            'LCL': '000000000000001',
            'ARG': '000000000000010',
           'THIS': '000000000000011',
           'THAT': '000000000000100',
             'R0': '000000000000000',
             'R1': '000000000000001',
             'R2': '000000000000010',
             'R3': '000000000000011',
             'R4': '000000000000100',
             'R5': '000000000000101',
             'R6': '000000000000110',
             'R7': '000000000000111',
             'R8': '000000000001000',
             'R9': '000000000001001',
            'R10': '000000000001010',
            'R11': '000000000001011',
            'R12': '000000000001100',
            'R13': '000000000001101',
            'R14': '000000000001110',
            'R15': '000000000001111',
         'SCREEN': '100000000000000',
            'KBD': '110000000000000',
        }


if __name__ == '__main__':
    import sys

    asm_filename = sys.argv[1]
    assembler = Assembler(Parser(), SymbolTable(), Code())
    assembler.assemble(asm_filename)
