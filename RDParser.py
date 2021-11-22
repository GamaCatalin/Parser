from Grammar import Grammar


class ParserRecursiveDescendent:
    def __init__(self, grammar_file, sequence_file, out_file):
        self.grammar = Grammar(grammar_file)
        self.sequence = self.read_sequence(sequence_file)
        print(self.sequence)
        self.out_file = out_file
        self.init_out_file()
        self.working = []
        self.input = [self.grammar.get_start_symbol()[0]]
        # q - forward state, b - back state, f - final state, e -error state
        self.state = "q"
        self.index = 0

        self.run()

    def read_sequence(self, seq_file):
        seq = []
        with open(seq_file) as f:
            line = f.readline()
            while line:
                elems_line = line.split("->")
                seq.append(elems_line[0])
                line = f.readline()
        return seq

    def init_out_file(self):
        f = open(self.out_file, 'w')
        f.write("")
        f.close()

    def write_status(self):
        with open(self.out_file, 'a') as f:
            f.write(str(self.state) + " ")
            f.write(str(self.index) + "\n")
            f.write(str(self.working) + "\n")
            f.write(str(self.input) + "\n")

    def write_in_out(self, message, final=False):
        with open(self.out_file, 'a') as f:
            if final:
                f.write("-------RESULT:-------\n")
            f.write(message + "\n")

    def run(self):
        pass
        while self.state != "f" or self.state != "e":
            self.write_status()
            if self.state == "q":
                if len(self.input) == 0 and self.index == len(self.sequence):
                    self.success()
                elif len(self.input) == 0:
                    self.error("No input, still have terminals to parse")
                    break
                else:
                    if self.input[0] in self.grammar.get_non_terminals():
                        self.expand()
                    else:
                        if self.index < len(self.sequence) and self.input[0] == self.sequence[self.index]:
                            self.advance()
                        else:
                            self.insuccess()
            else:
                if self.state == "b":
                    pass

    def success(self):
        self.write_in_out("---success---")
        self.state = "f"

    def error(self,msg):
        self.write_in_out(msg)
        print(msg)
        self.state = "e"

    def expand(self):
        self.write_in_out("---expand---")
        non_terminal = self.input.pop(0)
        self.working.append((non_terminal, 0))
        new_production = self.grammar.get_productions_for_non_terminal(non_terminal)[0]
        self.input[:0] = new_production

    def advance(self):
        pass

    def insuccess(self):
        pass


if __name__ == "__main__":
    parser = ParserRecursiveDescendent("g1.txt", "seq.txt", "out1.txt")
