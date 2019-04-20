import sys
from parser import Parser
from code import Code
from symbol_table import SymbolTable

def first_iter(table):
	filename = sys.argv[1].split('.')[0]
	asm_file = open(filename + '.asm', 'r')
	tmp_file = open(filename + '.tmp', 'w')

	line_number = 0

	for line in asm_file:
		line = line.strip()
		if line != "" and not line.startswith('//'):
			if line[0] == '(':
				label = line[1:-1]
				table.add_entry(label, line_number)
				line = ""
			else:
				line_number += 1
				tmp_file.write(line + "\n")

	asm_file.close()
	tmp_file.close()

def main():
	filename = sys.argv[1].split('.')[0]
	symbol_table = SymbolTable()
	first_iter(symbol_table)
	parser = Parser(filename)
	code = Code()
	output = []
	address = 16
	while(parser.has_more_commands()):
		parser.advance()

		if parser.command_type() == 'C_COMMAND':
			dest = parser.dest()
			comp = parser.comp()
			jump = parser.jump()
			# print(parser.current_command, code.dest(dest), code.comp(comp), code.jump(jump))
			output.append("111" + code.comp(comp) + code.dest(dest) + code.jump(jump))
		else:
			symbol = parser.symbol()

			try:
				symbol_address = int(symbol)
			except:
				if not symbol_table.contains(symbol):
					symbol_table.add_entry(symbol, address)
					address += 1
				symbol_address = symbol_table.get_address(symbol)
			finally:
				output.append(bin(symbol_address)[2:].zfill(16))
				# print(parser.current_command, bin(symbol_table.get_address(symbol)))

			# if not symbol_table.contains(symbol):
			# 	symbol_table.add_entry(symbol, address)
			# 	address += 1
			# 	symbol_address = symbol_table.get_address(symbol)
			# 	print(symbol_address)
			# 	output.append(bin(symbol_table.get_address(symbol))[2:].zfill(16))
			# 	print(parser.current_command, bin(symbol_table.get_address(symbol)))

			# print(symbol_address)
			# output.append(bin(symbol_table.get_address(symbol))[2:].zfill(16))
			# print(parser.current_command, bin(symbol_table.get_address(symbol)))

	parser.close()
	hack_file = open(filename + '.hack', 'w')
	for line in output:
		hack_file.write(line + '\n')
	hack_file.close()


if __name__ == '__main__':
	main()
