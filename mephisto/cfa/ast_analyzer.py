import ast

from .utils import read_lines


class FileProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.lines = read_lines(filename)

    def tokens(self):
        pass

    def build_ast(self) -> ast.AST:
        """Build an AST from the list of lines."""
        return ast.parse(''.join(self.lines))
