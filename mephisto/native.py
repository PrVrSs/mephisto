from mephisto.cfa import CFG
from mephisto.worker import worker


class FuzzerInput:
    def __iter__(self):
        return self

    def __next__(self):
        return 1


class CovAnalytic:
    def __init__(self):
        self._total_coverage: int = 0

    def __repr__(self) -> str:
        return ''


class Corpus:
    def __init__(self):
        self._data_generator = FuzzerInput()

    @property
    def input(self):
        return self._data_generator

    def analize(self, program_result):
        return

    def _generate_input(self):
        return 1

    def _initial_seed(self):
        return 0

    def feedback(self):
        c = self._initial_seed()

        while True:
            program_result = yield c
            # self.analize(program_result)
            c = self._generate_input()


class Native:

    def __init__(self):
        self._corpus = Corpus().feedback()

    def fuzz_one(self, data):
        NotImplementedError()

    def start(self, function):
        cfg = CFG().create(function)
        worker_result = worker(0, __callback__=function)

        print(list(cfg.as_line()))
        print(worker_result.trace_data)


def main():

    def simple(data):
        if data == 2:
            a = 7
        else:
            a = 3

        return 3

    Native().start(simple)


if __name__ == '__main__':
    main()
