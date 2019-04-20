import os

class Parser(object):
	def __init__(self, filename):
		self.filename = filename
		self.opened_file = None
		self.lines = []
		self.current_command = None
		self.open_file()

	def open_file(self):
		self.opened_file = open(self.filename + '.tmp', 'r')
		self.lines = [line.strip() for line in self.opened_file.readlines()]
		self.lines = [line for line in self.lines if not line.startswith('//') and line]

	def close(self):
		self.opened_file.close()
		os.remove(self.filename + '.tmp')

	def has_more_commands(self):
		return len(self.lines) > 0

	def advance(self):
		self.current_command = self.lines.pop(0)
		if "//" in self.current_command:
			self.current_command = self.current_command[:self.current_command.find('//')]
		self.current_command = self.current_command.replace(" ", "")
		# print(':'.join(hex(ord(x))[2:] for x in self.current_command))

	def command_type(self):
		if self.current_command[0] == '@':
			return 'A_COMMAND'
		elif self.current_command[0] == '(':
			return 'L_COMMAND'
		return 'C_COMMAND'

	def symbol(self):
		if self.command_type() == 'A_COMMAND':
			return self.current_command[1:]
		return self.current_command[1:-1]

	def dest(self):
		if '=' in self.current_command:
			return self.current_command[:self.current_command.find('=')]
		return 'null'

	def comp(self):
		if '=' in self.current_command:
			if ';' in self.current_command:
				return self.current_command[self.current_command.find('=')+1:self.current_command.find(';')]
			return self.current_command[self.current_command.find('=')+1:]
		elif ';' in self.current_command:
				return self.current_command[:self.current_command.find(';')]
		return self.current_command

	def jump(self):
		if ';' in self.current_command:
			return self.current_command[self.current_command.find(';')+1:]
		return 'null'
