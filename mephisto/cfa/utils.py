import difflib
import sys
import tokenize
from collections import deque
from dis import findlinestarts
from io import StringIO
from types import CodeType
from typing import List, Optional

from .constants import STDIN


def code_objects(code: CodeType):
    todo = deque([code])
    while todo:
        code = todo.pop()
        todo.extend(co_const for co_const in code.co_consts if isinstance(co_const, CodeType))
        yield code


def byte_parser(text: str):
    """Find the offsets in a byte code which are start of lines in the source."""
    return [
        lineno
        for code in code_objects(compile(text, '<str>', 'exec'))
        for _, lineno in findlinestarts(code)
    ]


def read_lines(filename: str) -> List[str]:
    if filename.lower() == STDIN:
        return _from_stdin()

    return _from_file(filename)


def diff_code(old_code: str, new_code: str, context: int, *, filename: Optional[str] = None) -> str:
    if old_code == new_code:
        return ''

    if filename:
        return '\n'.join(difflib.unified_diff(
            old_code.split('\n'),
            new_code.split('\n'),
            fromfile=filename,
            tofile=filename,
            lineterm='',
            n=context,
        ))

    return '\n'.join(
        difflib.unified_diff(old_code.split('\n'), new_code.split('\n'), lineterm='', n=context))


def _from_file(filename: str) -> List[str]:
    with tokenize.open(filename) as file:
        return file.readlines()


def _from_stdin() -> List[str]:
    return list(StringIO(sys.stdin.buffer.read().decode('utf-8')))
