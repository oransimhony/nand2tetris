import os

class Parser(object):
	def __init__(self, filename):
		self.filename = filename
		self.opened_file = None
		self.lines = []
		self.current_command = None
		self.open_file()

	def open_file(self):
		self.opened_file = open(self.filename + '.vm', 'r')
		self.lines = [line.strip() for line in self.opened_file.readlines()]
		self.lines = [line for line in self.lines if not line.startswith('//') and line]

	def close(self):
		self.opened_file.close()

	def has_more_commands(self):
		return len(self.lines) > 0

	def advance(self):
		self.current_command = self.lines.pop(0)
		if "//" in self.current_command:
			self.current_command = self.current_command[:self.current_command.find('//')]

	def command_type(self):
		if self.current_command.startswith('push'):
			return 'C_PUSH'
		elif self.current_command.startswith('pop'):
			return 'C_POP'
		return 'C_ARITHMETIC'

	def command(self):
		return self.current_command.split(' ')[0]

	def arg1(self):
		if self.command_type() == 'C_ARITHMETIC':
			return self.current_command
		elif self.command_type() != 'C_RETURN':
			return self.current_command.split(' ')[1]

	def arg2(self):
		arg2 = 0
		if self.command_type() == 'C_PUSH':
			arg2 = self.current_command.split(' ')[2]
		elif self.command_type() == 'C_POP':
			arg2 = self.current_command.split(' ')[2]
		elif self.command_type() == 'C_FUNCTION':
			arg2 = self.current_command.split(' ')[2]
		elif self.command_type() == 'C_CALL':
			arg2 = self.current_command.split(' ')[2]

		return int(arg2)
