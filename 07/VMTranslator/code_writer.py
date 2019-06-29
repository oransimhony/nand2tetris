class CodeWriter(object):
    def __init__(self, filename):
        self.count = 0
        self.filename = filename
        self.staticname = filename.split('/')[-1]
        self.opened_file = None
        self.open_file()
        self.push = '@SP\nA=M\nM=D\n@SP\nM=M+1'
        self.pop = '@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D'
        self.add = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M'
        self.sub = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D'
        # self.eq = '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@EQ.true.' + self.next_count() + '\nD;JEQ\n@SP\nA=M-1\nM=0\n@EQ.after.' + self.next_count() + '\n0;JMP\n(EQ.true.' + self.next_count() + ')\n@SP\nA=M-1\nM=-1\n(EQ.after.' + self.next_count() + ')'
        # self.lt = '@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@LT.true.' + self.next_count() + '\nD;JLT\n@SP\nA=M-1\nM=0\n@LT.after.' + self.next_count() + '\n0;JMP\n(LT.true.' + self.next_count() + ')\n@SP\nA=M-1\nM=-1\n(LT.after.' + self.next_count() + ')'
        # self.gt = '@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@GT.true.' + self.next_count() + '\n\nD;JGT\n@SP\nA=M-1\nM=0\n@GT.after.' + self.next_count() + '\n0;JMP\n(GT.true.' + self.next_count() + ')\n@SP\nA=M-1\nM=-1\n(GT.after.' + self.next_count() + ')'
        self.neg = '@SP\nA=M-1\nM=-M'
        self.and_ = '@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M'
        self.or_ = '@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M'
        self.not_ = '@SP\nA=M-1\nM=!M'

    def open_file(self):
        self.opened_file = open(self.filename + '.asm', 'w')

    def close(self):
        self.opened_file.close()

    def write_arithmetic(self, command):
        if command == 'add':
            self.write(self.add)
        elif command == 'sub':
            self.write(self.sub)
        elif command == 'eq':
            label = self.next_count()
            eq = '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@EQ.true.' + label + '\nD;JEQ\n@SP\nA=M-1\nM=0\n(EQ.true.' + label + ')'
            self.write(self.create_jump_command('EQ'))
        elif command == 'lt':
            label = self.next_count()
            lt = '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@LT.true.' + label + '\nD;JLT\n@SP\nA=M-1\nM=0\n(LT.true.' + label + ')'
            self.write(self.create_jump_command('LT'))
        elif command == 'gt':
            label = self.next_count()
            gt = '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@GT.true.' + label + '\nD;JGT\n@SP\nA=M-1\nM=0\n(GT.true.' + label + ')'
            self.write(self.create_jump_command('GT'))
        elif command == 'neg':
            self.write(self.neg)
        elif command == 'and':
            self.write(self.and_)
        elif command == 'or':
            self.write(self.or_)
        elif command == 'not':
            self.write(self.not_)
        else:
            print(command)

    def write_push_pop(self, command, segment, index):
        if segment == 'constant':
            self.write('@%d' % index)
            self.write('D=A')
            self.write(self.push)
        elif segment == 'local':
            if command == 'push':
                self.write('@LCL')
                self.write('D=M')
                self.write('@%d' % index)
                self.write('A=D+A')
                self.write('D=M')
                self.write(self.push)
            else:
                self.write('@LCL')
                self.write('D=M')
                self.write('@%d' % index)
                self.write('D=D+A')
                self.write(self.pop)
        elif segment == 'argument':
            if command == 'push':
                self.write('@ARG')
                self.write('D=M')
                self.write('@%d' % index)
                self.write('A=D+A')
                self.write('D=M')
                self.write(self.push)
            else:
                self.write('@ARG')
                self.write('D=M')
                self.write('@%d' % index)
                self.write('D=D+A')
                self.write(self.pop)
        elif segment == 'this':
            if command == 'push':
                self.write('@THIS')
                self.write('D=M')
                self.write('@%d' % index)
                self.write('A=D+A')
                self.write('D=M')
                self.write(self.push)
            else:
                self.write('@THIS')
                self.write('D=M')
                self.write('@%d' % index)
                self.write('D=D+A')
                self.write(self.pop)
        elif segment == 'that':
            if command == 'push':
                self.write('@THAT')
                self.write('D=M')
                self.write('@%d' % index)
                self.write('A=D+A')
                self.write('D=M')
                self.write(self.push)
            else:
                self.write('@THAT')
                self.write('D=M')
                self.write('@%d' % index)
                self.write('D=D+A')
                self.write(self.pop)
        elif segment == 'temp':
            if command == 'push':
                self.write('@R5')
                self.write('D=A')
                self.write('@%d' % index)
                self.write('A=D+A')
                self.write('D=M')
                self.write(self.push)
            else:
                self.write('@R5')
                self.write('D=A')
                self.write('@%d' % index)
                self.write('D=D+A')
                self.write(self.pop)
        elif segment == 'pointer':
            if command == 'push':
                self.write('@R3')
                self.write('D=A')
                self.write('@%d' % index)
                self.write('A=D+A')
                self.write('D=M')
                self.write(self.push)
            else:
                self.write('@R3')
                self.write('D=A')
                self.write('@%d' % index)
                self.write('D=D+A')
                self.write(self.pop)
        elif segment == 'static':
            if command == 'push':
                self.write('@%s.%d' % (self.staticname, index))
                self.write('D=M')
                self.write(self.push)
            else:
                self.write('@SP')
                self.write('M=M-1')
                self.write('A=M')
                self.write('D=M')
                self.write('@%s.%d' % (self.staticname, index))
                self.write('M=D')
        else:
            print(command, segment, index)

    def write(self, line):
        self.opened_file.write(line + '\n')

    def next_count(self):
        self.count += 1
        return str(self.count)

    def create_jump_command(self, command):
        label = self.next_count()
        return '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@' + command + '.true.' + label + '\nD;J' + command + '\n@SP\nA=M-1\nM=0\n(' + command + '.true.' + label + ')'

