#Brainfuck interpreter
#Author: Piotr Maślankowski, pmaslankowski@gmail.com

"""
Brainfuck interpreter.
Usage of script:
python brainfuck.py filepath_of_file_to_interpret.bf

This module consists Interpreter class.
"""

import sys
class Interpreter(object):
    """
    Interpreter class.

    Usage: create Interpreter object, pass path to brainfuck code file as
           constructor argument and call run method.
    """

    def __init__(self, filepath):
        """__init__(self, filepath) - filepath is path to file with brainfuck source code"""
        self._brackets = {}
        self.code = ""
        self.load(filepath)
        self._prepare()

    def load(self, filepath):
        """Loads code to self.code from filepath"""
        self.filepath = filepath
        with open(filepath, "r") as file:
            self.code = file.read().strip()

    def _prepare(self):
        """
        Functions finds matching brackets in code.
        As function's side effect, self.brackets is dictionary consisting indexes of
        matching brackets. For example: if [ is placed at i index, then matching ] is placed
        at self._brackets[i] index.
        """
        stack = []
        for i, c in enumerate(self.code):
            if c == '[':
                stack.append(('[', i))
            elif c == ']':
                bracket, j = stack.pop()
                if bracket != '[':
                    raise SyntaxError("Syntax error with brackets.")
                self._brackets[i] = j
                self._brackets[j] = i

    def run(self):
        """Brainfuck program main loop"""
        pc = 0 #program counter
        dp = 0 #data pointer
        data = [0] #data list
        end = False
        while not end:
            order = self.code[pc]
            if order == '>':
                dp += 1
                if dp == len(data):
                    data.append(0)
            elif order == '<':
                dp -= 1
            elif order == '+':
                data[dp] = data[dp] + 1 if data[dp] != 255 else 0
            elif order == '-':
                data[dp] = data[dp] - 1 if data[dp] != 0 else 255
            elif order == '.':
                print(chr(data[dp]), end="")
            elif order == ',':
                inp = input()
                data[dp] = ord(inp)
            elif order == '[':
                if data[dp] == 0:
                    pc = self._brackets[pc]
            elif order == ']':
                if data[dp] != 0:
                    pc = self._brackets[pc]
            pc += 1
            if pc == len(self.code):
                end = True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(sys.argv)
        print("Usage: python brainfuck.py filepath_of_file_to_interpret.bf")
    else:
        bf = Interpreter(sys.argv[1])
        bf.run()
