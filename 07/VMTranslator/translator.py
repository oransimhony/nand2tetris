import sys
from parser import Parser
from code_writer import CodeWriter

def main():
	filename = sys.argv[1].split('.')[0]
	parser = Parser(filename)
	code = CodeWriter(filename)
	while(parser.has_more_commands()):
		parser.advance()

		command_type = parser.command_type()

		if command_type == 'C_ARITHMETIC':
			code.write_arithmetic(parser.arg1())

		elif command_type == 'C_PUSH' or command_type == 'C_POP':
			code.write_push_pop(parser.command(), parser.arg1(), parser.arg2())

		# print(parser.current_command)
	parser.close()
	code.close()


if __name__ == '__main__':
	main()
