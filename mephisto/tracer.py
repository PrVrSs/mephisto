import dis
import sys
from collections import defaultdict
from types import FrameType
from typing import Any, Callable, Dict


LINE = 'line'
RETURN = 'return'
EXCEPTION = 'exception'
CALL = 'call'
YIELD_VALUE = dis.opmap['YIELD_VALUE']


class TraceData:

    def __init__(self):
        self._line = -1
        self._filename = ''
        self._last_exc_back = None
        self._last_exc_firstlineno = 0
        self._stack = []

        self.data = defaultdict(list)

        self._handlers: Dict[str, Callable[[FrameType], None]] = {
            CALL: self._call_handler,
            EXCEPTION: self._exception_handler,
            LINE: self._line_handler,
            RETURN: self._return_handler,
        }

    def add(self, frame: FrameType, event: str) -> None:
        if frame.f_code.co_filename == '<string>':
            return

        if self._last_exc_back:
            if frame == self._last_exc_back and self.data:
                self._save(self._filename, self._line, self._last_exc_firstlineno)  #
                self._filename, self._line = self._stack.pop()

            self._last_exc_back = None

        self._handlers[event](frame)

    def _save(self, filename: str, from_: int, to: int) -> None:
        self.data[filename].append((from_, to))

    def _line_handler(self, frame: FrameType) -> None:
        self._save(frame.f_code.co_filename, self._line, frame.f_lineno)
        self._line = frame.f_lineno

    def _return_handler(self, frame: FrameType) -> None:
        code = frame.f_code.co_code

        if not code or code[frame.f_lasti] != YIELD_VALUE:
            self._save(frame.f_code.co_filename, self._line, frame.f_code.co_firstlineno)  #

        self._filename, self._line = self._stack.pop()

    def _exception_handler(self, frame: FrameType) -> None:
        self._last_exc_back = frame.f_back
        self._last_exc_firstlineno = frame.f_code.co_firstlineno

    def _call_handler(self, frame: FrameType) -> None:
        self._stack.append((self._filename, self._line))

        line = self._get_call_line(frame)

        if self._line != - 1:
            self._save(frame.f_code.co_filename, self._line, line)

        self._line = line
        self._filename = frame.f_code.co_filename

    @staticmethod
    def _get_call_line(frame: FrameType) -> int:
        if getattr(frame, 'f_lasti', -1) < 0:
            return frame.f_code.co_firstlineno  #

        return frame.f_lineno


def skipped(frame: FrameType) -> bool:
    return __file__ == frame.f_code.co_filename


class Tracer:

    def __init__(self):
        self._data = TraceData()
        self._sys_trace = None

    def __enter__(self) -> 'Tracer':
        self._sys_trace = sys.gettrace()
        sys.settrace(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        sys.settrace(self._sys_trace)

    def __call__(self, frame: FrameType, event: str, _: Any) -> 'Tracer':
        return self._trace(frame, event)

    @property
    def data(self):
        return self._data.data

    def _trace(self, frame: FrameType, event: str) -> 'Tracer':
        if skipped(frame):
            return self

        self._data.add(frame, event)

        return self
