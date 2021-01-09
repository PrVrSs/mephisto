import dis
from itertools import chain, repeat
from operator import attrgetter

from more_itertools import first, first_true, last, pairwise


class Function:
    def __init__(self):
        self._blocks = []

    def new_block(self):
        self._blocks.append(block := Block())

        return block

    def find_by_offset(self, offsets):
        return [
            block
            for block in self._blocks
            if block.start_block_offset in offsets
        ]

    def as_line(self):
        for block in self._blocks:
            internal_lines = self.internal(block)

            yield from chain(
                pairwise(internal_lines),
                zip(repeat(last(internal_lines)), self.external(block.jump_offsets)),
            )

    def internal(self, block):
        return [
            instruction.starts_line
            for instruction in block.stack
            if instruction.starts_line is not None
        ]

    def external(self, jump_offsets):
        return [
            first_true(map(attrgetter('starts_line'), block.stack))
            for block in self.find_by_offset(jump_offsets)
        ]


class Block:
    def __init__(self):
        self.stack = []
        self.jump_offsets = []

    @property
    def start_block_offset(self):
        return first(self.stack).offset

    def add_instr(self, instr):
        self.stack.append(instr)
        self.jump_offsets = [instr.offset + 2]


class CFG:
    def __init__(self):
        self._function = Function()
        self._current_block = self._function.new_block()

        self._handlers = {
            'POP_JUMP_IF_FALSE': self._jump_if,
            'JUMP_FORWARD': self._jump_forward,
        }

    def _jump_if(self, inst):
        return [inst.offset + 2, inst.arg]

    def _jump_forward(self, inst):
        return [inst.argval]

    def create(self, code) -> Function:
        for i, ins in enumerate(dis.get_instructions(code)):
            if ins.is_jump_target:
                self._current_block = self._function.new_block()

            self._current_block.add_instr(ins)

            if jump_offset := self._handlers.get(ins.opname, lambda _: None)(ins):
                self._current_block.jump_offsets = jump_offset

            if ins.opname == 'POP_JUMP_IF_FALSE':
                self._current_block = self._function.new_block()

        return self._function


def test(a, b):
    if a < b:
        c = a
        a = b
    else:
        a = 5

    return a


def main():
    from mephisto.cfa.visualization import visualize
    v = CFG()
    g = v.create(test)

    visualize(list(g.as_line()))


if __name__ == '__main__':
    main()
